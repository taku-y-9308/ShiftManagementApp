#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

#デプロイ先がAWSかherokuでbindを変える
if [ $PLATFORM = "AWS" ]; then
    gunicorn config.wsgi --bind=unix:/var/run/gunicorn/gunicorn.sock
    echo "AWS"
elif [$PLATFORM = "heroku" ]; then
    gunicorn config.wsgi --bind=0.0.0.0:$PORT
    echo "heroku"
else
    gunicorn config.wsgi --bind=0.0.0.0:$PORT
fi