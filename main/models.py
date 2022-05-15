from tabnanny import verbose
from django.db import models

# Create your models here.
class Task(models.Model):
    hash = models.CharField('Hash of transaction:', max_length = 100)
    sender = models.CharField('Sender:', max_length = 100)
    receiver = models.CharField('Receiver:', max_length = 100)
    valueEth = models.CharField('Number of ETH:', max_length = 100)
    confirmation = models.CharField('Confirmation:', max_length = 100)
    exchangeName = models.CharField('Exchange place:', max_length = 100)

    def __str__(self):
        return self.hash
    
    class Meta:
        verbose_name = "ethAddress"
        verbose_name_plural = "ethAddresses"

class ethSearch(models.Model):
    target = models.CharField(max_length=100)

    def __str__(self):
        return self.target