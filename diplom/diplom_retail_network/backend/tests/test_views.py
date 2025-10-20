import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import User
from .factories import UserFactory

@pytest.mark.django_db
class TestUserViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = None

    def test_user_registration_success(self):
        #Тест успешной регистрации пользователя
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'StrongPassword123',
            'company': 'Test Company',
            'position': 'Manager'
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()

    def test_user_login_success(self):
        #Тест успешного входа пользователя
        user = UserFactory(email='login@test.com')
        user.set_password('testpass123')
        user.save()
        
        url = reverse('backend:user-login')
        data = {
            'email': 'login@test.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['Status'] is True
        assert 'Token' in response.json()
