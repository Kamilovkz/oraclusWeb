from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

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