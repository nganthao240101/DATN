from django.urls import path
from . import views
urlpatterns = [
    # Các URL khác của bạn
    path('/', views.flow_chart_view, name='flow_chart'),
]
