from django.contrib import admin
from .models import Task
from .models import ethSearch
from .models import uniSearch

admin.site.register(Task)
admin.site.register(ethSearch)
admin.site.register(uniSearch)

# Register your models here.
