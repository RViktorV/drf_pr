# Makefile

# Команда для запуска Celery worker
celery-worker:
		celery -A edu worker --loglevel=info

# Команда для запуска Celery beat
celery-beat:
		celery -A edu beat --loglevel=info

# Команда для перезапуска Celery worker и beat
restart-celery:
		make stop-celery
		make start-celery

# Команда для остановки Celery
stop-celery:
		pkill -f 'celery worker'
		pkill -f 'celery beat'

# Команда для запуска как Celery worker, так и beat
start-celery:
		make celery-worker &
		make celery-beat &
