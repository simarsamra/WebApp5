#!/bin/sh

set -e

python manage.py migrate
python manage.py collectstatic --noinput

echo "Press any key to run seed_data, or wait 30 seconds to skip..."
read -t 30 -n 1 key && SEED="yes" || SEED="no"

if [ "$SEED" = "yes" ]; then
    echo "Running seed_data..."
    python manage.py seed_data
else
    echo "Skipping seed_data."
fi

exec python -m uvicorn battery_manager.asgi:application --host 0.0.0.0 --port 8000