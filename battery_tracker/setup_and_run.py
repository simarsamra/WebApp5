import os
import subprocess
import sys
import venv

VENV_DIR = "venv"

def run(cmd, env=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, env=env)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def is_venv_active():
    # Checks if the script is running inside the venv
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        os.environ.get('VIRTUAL_ENV') is not None
    )

def is_installed(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False

def pkg_name(line):
    # Extract package name (handles version specifiers)
    return line.strip().split('==')[0].split('>=')[0].split('<=')[0].replace('-', '_')

def create_venv():
    if not os.path.isdir(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
        print(f"Virtual environment created in '{VENV_DIR}'.")
    else:
        print("Virtual environment already exists.")

def get_venv_python():
    if os.name == "nt":
        return os.path.abspath(os.path.join(VENV_DIR, "Scripts", "python.exe"))
    else:
        return os.path.abspath(os.path.join(VENV_DIR, "bin", "python"))

def install_requirements(python_exec):
    run(f'"{python_exec}" -m pip install --upgrade pip')
    run(f'"{python_exec}" -m pip install -r requirements.txt')

def ensure_superuser(python_exec):
    import getpass
    # Check if any user exists
    check_user_cmd = (
        f'"{python_exec}" manage.py shell -c "from django.contrib.auth import get_user_model; '
        f'exit(0) if get_user_model().objects.exists() else exit(1)"'
    )
    result = subprocess.run(check_user_cmd, shell=True)
    if result.returncode == 0:
        print("At least one user exists. Skipping superuser creation.")
        return

    print("No users found. Creating a superuser.")
    username = input("Enter superuser username: ")
    email = input("Enter superuser email: ")
    while True:
        password = getpass.getpass("Enter superuser password: ")
        password2 = getpass.getpass("Confirm password: ")
        if password == password2:
            break
        print("Passwords do not match. Try again.")

    # Use Django shell to create the superuser
    create_superuser_cmd = (
        f'"{python_exec}" manage.py shell -c "'
        f'from django.contrib.auth import get_user_model; '
        f'User = get_user_model(); '
        f'User.objects.create_superuser(\'{username}\', \'{email}\', \'{password}\')"'
    )
    run(create_superuser_cmd)

def main():
    if not os.path.isdir(VENV_DIR):
        print("Virtual environment not found. Creating one...")
        venv.create(VENV_DIR, with_pip=True)
        print(f"Virtual environment created in '{VENV_DIR}'.")
        print(f"Please activate the virtual environment and re-run this script:")
        if os.name == "nt":
            print(rf"    {VENV_DIR}\Scripts\activate")
        else:
            print(rf"    source {VENV_DIR}/bin/activate")
        sys.exit(0)
    elif not is_venv_active():
        print("Virtual environment exists but is not activated.")
        print(f"Please activate the virtual environment and re-run this script:")
        if os.name == "nt":
            print(rf"    {VENV_DIR}\Scripts\activate")
        else:
            print(rf"    source {VENV_DIR}/bin/activate")
        sys.exit(0)

    python_exec = get_venv_python()
    install_requirements(python_exec)

    os.chdir("battery_manager")
    run(f'"{python_exec}" manage.py migrate')
    run(f'"{python_exec}" manage.py collectstatic --noinput')
    # run(f'"{python_exec}" manage.py seed_data')  # Optional

    ensure_superuser(python_exec)

    run(f'"{python_exec}" -m uvicorn battery_manager.asgi:application --host 0.0.0.0 --port 8000')

if __name__ == "__main__":
    main()