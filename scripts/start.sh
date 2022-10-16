echo "$(tput setaf 4) Starting celery...$(tput init)"

cd backend || exit

celery -A app.celery worker --loglevel=info  &

echo "$(tput setaf 4)Starting flask server...$(tput init)"

python3 app.py
