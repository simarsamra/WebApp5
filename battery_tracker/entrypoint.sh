#!/bin/sh
# filepath: c:\Users\simar\Documents\WebAppContainer\WebApp5\battery_tracker\entrypoint.sh

set -e

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optional: Seed data
echo "-----------------------------------------------------"
echo "Press 'y' to run seed_data, or wait 30 seconds to skip..."
echo "-----------------------------------------------------"
# Use -r to prevent backslash interpretation, ensure key_seed is reset
key_seed=""
read -t 30 -n 1 -r key_seed_input && key_seed=$(echo "$key_seed_input" | tr '[:upper:]' '[:lower:]') || key_seed="timeout"

if [ "$key_seed" = "y" ]; then
    echo # Newline after key press
    echo "Running seed_data..."
    python manage.py seed_data
else
    echo # Newline after timeout or if no key pressed
    echo "Skipping seed_data."
fi

# Optional: Create superuser if none exists
echo "-----------------------------------------------------"
echo "Checking for existing users..."
# Check if any user exists. Exit code 0 means users exist, 1 means no users.
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.exists() else exit(1)"; then
    echo "User(s) already exist. Skipping superuser creation prompt."
else
    echo "No users found in the database."
    echo "Press 'y' to create a default superuser, or wait 30 seconds to skip..."
    echo "Default credentials (can be overridden by ENV VARS):"
    echo "  Username: \${DJANGO_SUPERUSER_USERNAME:-admin}"
    echo "  Email:    \${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
    echo "  Password: \${DJANGO_SUPERUSER_PASSWORD:-password} (CHANGE THIS IN PRODUCTION)"
    echo "-----------------------------------------------------"
    key_superuser_create_prompt=""
    read -t 30 -n 1 -r key_superuser_input && key_superuser_create_prompt=$(echo "$key_superuser_input" | tr '[:upper:]' '[:lower:]') || key_superuser_create_prompt="timeout"

    if [ "$key_superuser_create_prompt" = "y" ]; then
        echo # Newline
        # Use environment variables for credentials if set, otherwise use defaults
        SU_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
        SU_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
        SU_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-password}

        echo "Creating superuser: Username=$SU_USERNAME, Email=$SU_EMAIL ..."
        # Create superuser using Django shell to bypass interactive prompts and set password
        echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$SU_USERNAME', '$SU_EMAIL', '$SU_PASSWORD')" | python manage.py shell
        echo "Default superuser created."
    else
        echo # Newline
        echo "Skipping default superuser creation."
    fi
fi
echo "-----------------------------------------------------"

# Start Uvicorn server
echo "Starting Uvicorn server on 0.0.0.0:8000..."
exec python -m uvicorn battery_manager.asgi:application --host 0.0.0.0 --port 8000