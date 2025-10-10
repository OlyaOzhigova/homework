from django.urls import path
from . import views

app_name = 'backend'
urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('import/', views.ImportProducts.as_view(), name='import-products'),
    path('import/force/', views.ImportProductsForce.as_view(), name='import-products-force'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('shops/', views.ShopView.as_view(), name='shops'),
    path('products/', views.ProductInfoView.as_view(), name='products'),
]
