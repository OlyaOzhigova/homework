from django.urls import path
from .views import SensorView, SensorDetailView, MeasurementView

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<int:pk>/', SensorDetailView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]