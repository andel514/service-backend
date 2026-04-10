web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput