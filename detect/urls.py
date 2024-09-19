from django.urls import path
from . import views

urlpatterns = [
    path('/', views.detect_view, name='detect'),
    path('/test', views.index, name='test'),
    path('/detect-data', views.detect_filter, name='detect_filter'),
    path('/logpcap_filter_time', views.logpcap_filter_time, name='detectFilterTimeUrl'),
]
