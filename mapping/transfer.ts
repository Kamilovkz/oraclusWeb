import { Exchange } from "../generated/schema";
import { Transfer } from "../generated/Transfer/UNISWAP";

function handleTransfer(event: Transfer): void {
    let transfer = Exchange.load(event.transaction.hash.toHex());
    if (transfer == null) {
        transfer = new Exchange(event.hash.transaction.hash.toHex());
    }
    transfer.block = event.block.number;
    transfer.from = event.params.from.toHex();
    transfer.to = event.params.to.toHex();
    transfer.amount = event.params.value;
    
    transfer.save();
}