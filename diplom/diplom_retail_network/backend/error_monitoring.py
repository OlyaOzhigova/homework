import logging
import traceback
from datetime import datetime
import os
from django.conf import settings
import json

logger = logging.getLogger(__name__)

class ErrorMonitor:
    """
    локальный мониторинг ошибок(сохранение в файл)
    """
    
    @staticmethod
    def capture_exception(error, context=None):
        """
        Захватывает исключение и сохраняет информацию о нем
        """
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'level': 'error'
        }
        
        # Логируем ошибку
        logger.error(f"Error captured: {error_info['error_type']}: {error_info['error_message']}")
        
        # Сохраняем в файл для дальнейшего анализа
        ErrorMonitor._save_to_jsonl('errors', error_info)
        
        return error_info
    
    @staticmethod
    def capture_message(message, level='info', context=None):
        """
        Захватывает произвольное сообщение
        """
        message_info = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'context': context or {}
        }
        
        # Логируем в зависимости от уровня
        if level == 'error':
            logger.error(message)
        elif level == 'warning':
            logger.warning(message)
        else:
            logger.info(message)
            
        ErrorMonitor._save_to_jsonl('messages', message_info)
        
        return message_info
    
    @staticmethod
    def _save_to_jsonl(log_type, data):
        """Сохраняет ошибку в файл"""
        try:
            log_dir = os.path.join(settings.BASE_DIR, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f'{log_type}.jsonl')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Failed to save to {log_type} log: {e}")
    
    @staticmethod
    def get_recent_errors(limit=10):
        """Сохраняет сообщение в файл"""
        try:
            log_file = os.path.join(settings.BASE_DIR, 'logs', 'errors.jsonl')
            if not os.path.exists(log_file):
                return []
                
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-limit:]
                return [json.loads(line) for line in lines]
        except Exception as e:
            logger.error(f"Failed to read errors: {e}")
            return []

# Алиасы для Sentry-like API
def capture_exception(error, context=None):
    return ErrorMonitor.capture_exception(error, context)

def capture_message(message, level='info', context=None):
    return ErrorMonitor.capture_message(message, level, context)
