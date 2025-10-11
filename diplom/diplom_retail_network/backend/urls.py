from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from . import views

app_name = 'backend'
urlpatterns = [
    """ ===== ПОЛЬЗОВАТЕЛИ ===== """
    #регистрация пользователя
    path('user/register', views.RegisterAccount.as_view(), name='user-register'),
    
    #авторизация пользователя(тоекн)
    path('user/login', views.LoginAccount.as_view(), name='user-login'),
    
    #просмотр и редаутирование данных пользователя
    path('user/details', views.AccountDetails.as_view(), name='user-details'),  
    
    #сброс пароля (email+токен)
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    
    #подтверждение сброса пароля (email+токен)
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),

    """ ===== ПОСТАВЩИКИ ===== """
    #добавление , обновление товароа
    path('partner/update', views.ImportProducts.as_view(), name='partner-update'),
    #обновление, удаление старызх данных
    path('partner/update/force', views.ImportProductsForce.as_view(), name='partner-update-force'),


    """ ===== ТОВАРЫ ===== """
    #получение всех категорий
    path('categories', views.CategoryView.as_view(), name='categories'),
    
    #получение списка поставщиков 
    path('shops', views.ShopView.as_view(), name='shops'),
    
    #поиск и фильтрация товаров
    path('products', views.ProductInfoView.as_view(), name='products'),

    """ ===== ЗАКАЗЫ и КОРЗИНА ===== """
    
    #корзина(просмотр, добавление, удаление, обновление)
    path('basket', views.BasketView.as_view(), name='basket'),

    #адреса доставки(просмотр, добавление, удаление)
    path('contact', views.ContactView.as_view(), name='contact'),

    #заказ (оформление, просмотр истории)
    path('order', views.OrderView.as_view(), name='order'),

    #для теста
    path('test', views.test_view, name='test'),
]
