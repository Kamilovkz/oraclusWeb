from dataclasses import fields

from matplotlib import widgets
from .models import Task
from django.forms import ModelForm, TextInput

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["hash", "sender", "receiver", "valueEth", "confirmation", "exchangeName"]
        widgets = {
            "hash": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter hash'
        }),
            "sender": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter sender'
        }),
            "receiver": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter receiver'
        }),
            "valueEth": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter valueEth'
        }),
            "confirmation": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter confirmation'
        }),
            "exchangeName": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter exchangeName'
        }),
        

        }