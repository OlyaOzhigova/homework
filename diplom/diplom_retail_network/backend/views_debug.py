from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .error_monitoring import capture_exception, capture_message

logger = logging.getLogger(__name__)

class TestErrorView(APIView):
    """
    View для тестирования мониторинга ошибок (вместо Sentry)
    """
    
    def get(self, request):
        # Логируем разные уровни сообщений
        logger.debug("Debug message - для отладки")
        logger.info("Info message - информационное сообщение")
        logger.warning("Warning message - предупреждение")
        logger.error("Error message - ошибка")
        
        # Захватываем сообщение через наш мониторинг
        capture_message("Тестовое сообщение через ErrorMonitor", level='info')
        
        # Вызываем исключение для теста мониторинга
        if request.GET.get('error'):
            try:
                # Генерируем исключение
                raise ValueError("Это тестовая ошибка для проверки мониторинга!")
            except Exception as e:
                # Забираем исключение
                error_info = capture_exception(e, {
                    'user_id': request.user.id if request.user.is_authenticated else None,
                    'endpoint': '/api/debug/sentry-test',
                    'query_params': dict(request.GET)
                })
                
                return Response({
                    'status': 'error',
                    'message': 'Исключение было захвачено системой мониторинга',
                    'error_id': id(error_info),  # Простой ID для отслеживания
                    'error_type': type(e).__name__
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Тестируем разные сценарии
        if request.GET.get('warning'):
            capture_message("Тестовое предупреждение", level='warning', context={
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'ip_address': request.META.get('REMOTE_ADDR')
            })
            
        return Response({
            'status': 'ok', 
            'message': 'Система мониторинга ошибок работает',
            'endpoints': {
                'test_error': '/api/debug/sentry-test?error=1',
                'test_warning': '/api/debug/sentry-test?warning=1',
                'view_logs': 'file:///home/vboxuser/homework/diplom/diplom_retail_network/logs/'
            }
        })

class PerformanceTestView(APIView):
    """
    View для тестирования производительности и кэширования
    """
    
    def get(self, request):
        from django.core.cache import cache
        from backend.models import ProductInfo
        import time
        
        # Тест кэширования
        cache_key = 'performance_test'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            # Данные из кэша
            return Response({
                'status': 'from_cache',
                'data': cached_data,
                'message': 'Данные загружены из кэша'
            })
        else:
            # Имитация тяжелого запроса
            time.sleep(1)
            data = {
                'timestamp': time.time(),
                'products_count': ProductInfo.objects.count(),
                'message': 'Данные загружены из базы и сохранены в кэш'
            }
            
            # Сохраняем в кэш 5 минут
            cache.set(cache_key, data, 300)
            
            return Response({
                'status': 'from_database', 
                'data': data,
                'message': 'Данные загружены из базы и сохранены в кэш'
            })
