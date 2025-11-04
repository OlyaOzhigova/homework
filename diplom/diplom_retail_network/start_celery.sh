echo "Starting Celery Worker..."
celery -A netology_pd_diplom worker --loglevel=info --pool=solo &

echo "Starting Celery Beat (if needed)..."
celery -A netology_pd_diplom beat --loglevel=info &

echo "Starting Flower (monitoring)..."
celery -A netology_pd_diplom flower --port=5555 &
