import pytest
from django.urls import reverse
from rest_framework import status
from backend.models import User

@pytest.mark.django_db
class TestAdditionalViews:
    def test_import_products(self, api_client):
        """Тест импорта товаров"""
        user = User.objects.create_user(
            email='shop@test.com', 
            password='testpass123',
            type='shop'
        )
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:partner-update')
        response = api_client.post(url)
        
        # вернется 200 или 400 (наличие файла)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_password_reset(self, api_client):
        """Тест сброса пароля"""
        # Сначала создадим пользователя
        user = User.objects.create_user(
            email='reset@test.com',
            password='oldpassword123'
        )
        
        url = reverse('backend:password-reset')
        data = {'email': 'reset@test.com'}
        
        response = api_client.post(url, data)
        # 200(пользователь существует)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['status'] == 'OK'
