release: python manage.py makemigrations  # todo remove in production
release: python manage.py migrate
web: gunicorn BosvogelWebPlatform.wsgi --log-file -