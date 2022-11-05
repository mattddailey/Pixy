# Make script work regardless of where it is run from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}/.." || exit

echo "$(tput setaf 4)Starting react app...$(tput init)"

cd frontend || exit

npm start &

echo "$(tput setaf 4)Starting celery...$(tput init)"

cd ../backend || exit


redis-server &
celery -A app.celery worker --loglevel=info  &

echo "$(tput setaf 4)Starting flask server...$(tput init)"

flask run --host 0.0.0.0
