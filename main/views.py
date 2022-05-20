import requests
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

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
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=' + keyApi 
    
    ethAddresses = ethSearch.objects.all()
    print(ethAddresses)

    all_addresses = []
    for targetAddress in ethAddresses:
        res = requests.get(url.format(targetAddress)).json()
        jsonTbl = res["result"]
        i = 0
        for result_item in jsonTbl:
            item_dict = jsonTbl[i]
            print("From: " + item_dict["from"])
            i = i + 1
            
        
        # target_address = {
        #     'hash': res["result"][0]["hash"],
        #     'sender': res["result"][0]["from"],
        #     'receiver': res["result"][0]["to"],
        #     'valueEth': res["result"][0]["value"],
        #     'confirmation': res["result"][0]["confirmations"]
        # }
        # all_addresses.append(target_address)

    information = {'all_info': all_addresses}




    return render(request, 'main/ethapi.html', information)

    