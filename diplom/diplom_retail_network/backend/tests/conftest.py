import pytest
from rest_framework.test import APIClient
from django.conf import settings

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def disable_throttling():
    """троттлинг для всех тестов отключено"""
    if hasattr(settings, 'REST_FRAMEWORK'):
        original_rates = settings.REST_FRAMEWORK.get('DEFAULT_THROTTLE_RATES', {})
        settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
            'user': '1000/minute',
            'anon': '1000/minute'
        }
        yield
        settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = original_rates
    else:
        yield
