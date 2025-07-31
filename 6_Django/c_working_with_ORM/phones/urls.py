from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.show_catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.show_product, name='phone'),
    path('', views.index, name='home'),
]