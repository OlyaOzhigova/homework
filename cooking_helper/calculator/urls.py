from django.urls import path
from . import views

urlpatterns = [
    path('<str:dish>/', views.recipe_view, name='recipe'),
]