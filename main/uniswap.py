# infura_url = 'https://mainnet.infura.io/v3/4ab138954e4e4b419660fa9a4c5e7e17'
# web3 = Web3(Web3.HTTPProvider(infura_url))

# uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
# uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
# uniswap_factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)

from functools import partial
from multiprocessing import Pool

from web3._utils.filters import construct_event_filter_params
from web3._utils.events import get_event_data
from web3 import Web3
import os
import json
import time
from hexbytes import HexBytes

import requests
from dotenv import dotenv_values

ETHERSCAN = "https://api.etherscan.io/api"

def config() -> dict:
    return dict(os.environ)

def get_web3(conn_type: str = "https") -> Web3:
    conf = config()
    if conn_type == "ws":
        return Web3(
            Web3.WebsocketProvider("wss://mainnet.infura.io/v3/4ab138954e4e4b419660fa9a4c5e7e17")
        )
    else:
        return Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/4ab138954e4e4b419660fa9a4c5e7e17"))

def read_abi(filename: str, address: str = False) -> dict:
    # try reading file if exists
    json_path = os.path.join(os.getcwd(), "src", "abi", f"{filename}.json")
    try:
        with open(json_path) as f:
            abi = json.load(f)

    # if doesn't and address is known, use that instead
    except:
        abi = get_abi_etherscan(address)
        try:
            with open(json_path, "w") as f:
                f.write(abi)
        except:
            return abi
    return abi

def get_abi_etherscan(address):
    # lag to not exceed rate limit by accident
    time.sleep(0.3)
    conf = config()

    # save as address if not found
    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        # "apikey": conf["etherscan"],
    }
    r = requests.get(ETHERSCAN, params=params)
    abi = r.json()["result"]
    return abi

def get_ws_endpoint() -> str:
    conf = config()
    return f"wss://mainnet.infura.io/ws/v3/{conf['infura']}"

def create_topic_string(abi: dict, eventname: str) -> str:
    """
    Parses ABI to create a "topic string" used as input in some web3 functions
    Not tested and likely fails with e.g. structs
    """

    topic_string = f"{eventname}("
    for i in abi:
        if "name" in i and "type" in i:
            if i["name"] == eventname and i["type"] == "event":
                for j in i["inputs"]:
                    topic_string += f"{j['internalType']},"
    topic_string = f"{topic_string[:-1]})"
    return topic_string

def convert_ws_response(res):
    """
    Tailor-made to convert the websocket response into correct format accepted by "get_event_data"
    Not tested and might fail in some scenarios
    """
    w3 = get_web3()
    return {
        "address": res["address"],
        "blockHash": HexBytes(res["blockHash"]),
        "blockNumber": w3.toInt(hexstr=res["blockNumber"]),
        "data": res["data"],
        "logIndex": w3.toInt(hexstr=res["logIndex"]),
        "removed": res["removed"],
        "topics": [HexBytes(item) for item in res["topics"]],
        "transactionHash": HexBytes(res["transactionHash"]),
        "transactionIndex": w3.toInt(hexstr=res["transactionIndex"]),
    }




# UNDER IT'S CODE


def create_interval_list(
    from_block: int,
    to_block: int,
    interval: int
    ) -> list:
    """
    Creates even intervals where last one is cut to match total blocks
    """
    intervals = []
    current_block = from_block
    while current_block < to_block:
        intervals.append(
            (int(current_block), int(min(current_block + interval, to_block)))
        )
        current_block += interval + 1

    return intervals

def _read_interval(
    address: list,
    abi: dict,
    event_name: str,
    argument_filters: dict,
    interval: tuple
) -> list:
    """reads specific events in interval from specific contract"""

    """
    Should be updated so that each interval does not need to create objects
    but there are problems when trying to run multithread
    """
    w3 = get_web3()
    from_block, to_block = interval
    contract = w3.eth.contract(address=address, abi=abi)
    event = contract.events.__getitem__(event_name)
    event_abi = event._get_event_abi()
    abi_codec = event.web3.codec
    topic_hash = None

    current_block = from_block
    chunksize = to_block - from_block
    adjustment = 1

    all_logs = []
    while current_block < to_block:
        try:

            data_filter_set, event_filter_params = construct_event_filter_params(
                event_abi,
                abi_codec,
                contract_address=event.address,
                argument_filters=argument_filters,
                fromBlock=current_block,
                toBlock=int(min(to_block, current_block + chunksize / adjustment)),
                address=address,
                topics=topic_hash,
            )
            logs = w3.eth.get_logs(event_filter_params)
            all_logs += logs
            adjustment = 1
            current_block = event_filter_params["toBlock"] + 1

        except Exception as e:
            print("ERROR", e)
            adjustment *= 2

    return all_logs


def read_history(
    address: str,
    abi: dict,
    event_name: str,
    from_block: int,
    to_block: int,
    interval: int,
    argument_filters: dict,
) -> list:
    """
    coordinates reading historical events through threads
    """
    intervals = create_interval_list(from_block, to_block, interval)
    with Pool(20) as p:
        log_lists = p.map(
            partial(_read_interval, address, abi, event_name, argument_filters),
            intervals,
        )

    logs = [item for sublog in log_lists for item in sublog]
    parsed_events = []

    contract = get_web3("https").eth.contract(address=address, abi=abi)
    event = contract.events.__getitem__(event_name)
    event_abi = event._get_event_abi()
    abi_codec = event.web3.codec

    for event in logs:
        parsed_events.append(get_event_data(abi_codec, event_abi, event))
    return parsed_events

if __name__ == "__main__":
    w3 = get_web3("https")
    # address = w3.toChecksumAddress("0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852")
    # abi = read_abi("uni_v2_pool", address=pool_address)

    # address = w3.toChecksumAddress("0x6B175474E89094C44Da98b954EedeAC495271d0F")
    # abi = read_abi("erc20", address=address)

    address = w3.toChecksumAddress("0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc")
    abi = read_abi("uni_v2_pool", address=address)

    contract = w3.eth.contract(address=address, abi=abi)

    event = contract.events.__getitem__("Sync")
    event_abi = event._get_event_abi()
    abi_codec = event.web3.codec

    event_logs = read_history(address, abi, "Sync", 14504000, 14507042, 10000, {})
    print(f"Found total of {len(event_logs)} events")
