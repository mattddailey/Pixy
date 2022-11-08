ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
ps auxww | grep flask | awk '{print $2}' | xargs kill -9
