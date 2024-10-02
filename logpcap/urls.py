from django.urls import path
from . import views

urlpatterns = [
    path('/', views.logpcap_view, name='logpcap'),
    path('/load-data', views.logpcap_filter, name='logpcap_filter'),
    path('/get-chart-data', views.get_chart_data, name='get_chart_data'),
]
