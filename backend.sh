# Gunicorn implementation 
gunicorn --bind 0.0.0.0:3000 wsgi:app -t 3600 -w 1