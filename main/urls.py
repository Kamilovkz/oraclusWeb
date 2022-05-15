from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about-project', views.about, name='about'),
    path('create', views.create, name='create'),
    path('ethapi', views.api, name='ethapi')
]
