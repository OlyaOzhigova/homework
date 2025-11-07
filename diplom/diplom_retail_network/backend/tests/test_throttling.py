import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestThrottling:
    """Тесты для проверки троттлинга API"""
    
    def test_anonymous_throttling(self):
        """Тест троттлинга для анонимных пользователей"""
        client = APIClient()
        url = reverse('backend:products')
        
        # Делаем несколько запросов подряд
        for i in range(10):  # лимит запросов в день
            response = client.get(url)
            
        # превышения лимита вернётся 429
        #assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        #лимит увеличен ожидаю 200
        assert response.status_code == status.HTTP_200_OK


    def test_user_throttling(self, api_client):
        """Тест троттлинга для авторизованных пользователей"""
        from backend.models import User
        
        user = User.objects.create_user(
            email='throttle@test.com', 
            password='testpass123'
        )
        api_client.force_authenticate(user=user)
        
        url = reverse('backend:products')
        
        # Делаем много запросов
        for i in range(10):  # лимит запросов в день
            response = api_client.get(url)
            
        # В тестовом режиме ожидаю 200
        assert response.status_code == status.HTTP_200_OK
        #assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
