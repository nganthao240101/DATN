from django.urls import path
from . import views

urlpatterns = [
    path('/', views.logpfsense_view, name='logpfsense'),
    path('/call_logpfsense', views.call_logpfsense, name='call_logpfsense'),
]
