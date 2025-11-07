import pytest
from django.urls import reverse
from rest_framework import status
import os
from django.conf import settings

@pytest.mark.django_db
class TestErrorMonitoring:
    """система мониторинга ошибок"""
    
    def test_error_capture(self, api_client):
        """ошибка"""
        url = reverse('backend:error-test')
        response = api_client.get(url, {'error': '1'})
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert 'error_id' in response.json()
        
        # Проверяем, что файл лога создан
        log_dir = os.path.join(settings.BASE_DIR, 'logs')
        assert os.path.exists(log_dir)
    
    def test_performance_cache(self, api_client):
        """кэширование производительности"""
        url = reverse('backend:performance-test')
        
        # Первый запрос
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        # Второй запрос
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
