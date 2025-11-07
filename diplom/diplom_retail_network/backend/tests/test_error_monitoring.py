import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import os
from django.conf import settings

@pytest.mark.django_db
class TestErrorMonitoring:
    """Тесты для системы мониторинга ошибок (вместо Sentry)"""
    
    def test_error_capture(self, api_client):
        """Тест захвата ошибки"""
        url = reverse('backend:error-test')
        response = api_client.get(url, {'error': '1'})
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert 'error_id' in response.json()
        
        # Проверяем, что файл лога создан
        log_dir = os.path.join(settings.BASE_DIR, 'logs')
        assert os.path.exists(log_dir)
    
    def test_performance_cache(self, api_client):
        """Тест кэширования производительности"""
        url = reverse('backend:performance-test')
        
        # Первый запрос - из базы
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json()['status'] == 'from_database'
        
        # Второй запрос - из кэша
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()['status'] == 'from_cache'
