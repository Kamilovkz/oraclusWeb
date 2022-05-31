from xml.sax.handler import feature_string_interning
import requests
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from .models import uniSearch
from .models import ethSearch

# Create your views here.
def index(request):
    cryptos = Task.objects.all()
    return render(request, 'main/index.html', {'title': 'OraclusWeb', 'cryptos': cryptos})



def about(request):
    return render(request, 'main/about.html')

def create(request):
    error = ""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Form is invalid'
    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)

def api(request):
    keyApi = 'AXJCAMW4DHQ3K7V3W2TZ2ZMGJ6QSVDU2F6'
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey=' + keyApi 
    
    ethAddresses = ethSearch.objects.all()
    # print(ethAddresses)

    all_addresses = []
    for targetAddress in ethAddresses:
        res = requests.get(url.format(targetAddress)).json()
        jsonTbl = res["result"]
        # print(jsonTbl)
        i = 0
        for result_item in jsonTbl:
            item_dict = jsonTbl[i]
            # print("From: " + item_dict["from"])
            i = i + 1
            target_address = {
                'hash': item_dict["hash"],
                'sender': item_dict["from"],
                'receiver': item_dict["to"],
                'valueEth': item_dict["value"],
                'confirmation': item_dict["confirmations"]
            }
            all_addresses.append(target_address)

    information = {'all_info': all_addresses}

    return render(request, 'main/ethapi.html', information)

def uniswap(request):
    keyApiUni = '1ATJAHX769A7VQYUXDUU3SYCUQP8IMCFHZ'
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey=' + keyApiUni 
    
    uniAddresses = uniSearch.objects.all()
    # print(ethAddresses)

    all_addresses2 = []
    for targetAddress2 in uniAddresses:
        res = requests.get(url.format(targetAddress2)).json()
        jsonTbl2 = res["result"]
        # print(jsonTbl2)
        i = 0
        for result_item in jsonTbl2:
            item_dict2 = jsonTbl2[i]
            # print("VAlue: " + item_dict["value"])
            i = i + 1
            target_address2 = {
                'hash': item_dict2["hash"],
                'sender': item_dict2["from"],
                'receiver': item_dict2["to"],
                'valueEth': item_dict2["value"],
                'confirmation': item_dict2["confirmations"],
                'to': item_dict2['to']
            }
            all_addresses2.append(target_address2)

    information = {'all_info': all_addresses2}

    return render(request, 'main/uniswap.html', information)
    