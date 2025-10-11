from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from . import views

app_name = 'backend'
urlpatterns = [
    path('user/register', views.RegisterAccount.as_view(), name='user-register'),
    path('user/login', views.LoginAccount.as_view(), name='user-login'),
    path('user/details', views.AccountDetails.as_view(), name='user-details'),  
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    
    path('partner/update', views.ImportProducts.as_view(), name='partner-update'),
    path('partner/update/force', views.ImportProductsForce.as_view(), name='partner-update-force'),
    
    path('categories', views.CategoryView.as_view(), name='categories'),
    path('shops', views.ShopView.as_view(), name='shops'),
    path('products', views.ProductInfoView.as_view(), name='products'),
    
    path('basket', views.BasketView.as_view(), name='basket'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('order', views.OrderView.as_view(), name='order'),
    
    path('test', views.test_view, name='test'),
]
