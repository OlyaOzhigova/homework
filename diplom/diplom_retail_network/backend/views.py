from django.http import JsonResponse
from rest_framework.views import APIView

class TestView(APIView):
    def get(self, request):
        return JsonResponse({'status': 'API is working!', 'message': 'Django is running successfully'})
