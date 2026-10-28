from django.urls import path
from . import views

urlpatterns = [
    path('healthz/', views.health_check, name='health_check'),
    path('', views.home, name='home'),
    path('data.csv', views.export_predictions_csv, name='export_predictions_csv'),
    path('data.json', views.export_predictions_json, name='export_predictions_json'),
]