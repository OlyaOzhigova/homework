echo "Stopping existing Celery processes..."
pkill -f "celery worker" || true
sleep 2

echo "Starting Redis..."
redis-server --daemonize yes

echo "Starting Celery Worker..."
celery -A netology_pd_diplom worker --loglevel=info --pool=solo &

echo "Waiting for worker to start..."
sleep 5

echo "Starting Celery Beat (if needed)..."
celery -A netology_pd_diplom beat --loglevel=info &

echo "Starting Flower (monitoring)..."
celery -A netology_pd_diplom flower --port=5555 --broker=redis://localhost:6379/0 &

echo "Celery processes started:"
ps aux | grep celery

echo "Flower should be available at: http://localhost:5555"
