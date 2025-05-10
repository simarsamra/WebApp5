import os
import subprocess
import sys

def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def is_installed(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False

def pkg_name(line):
    # Extract package name (handles version specifiers)
    return line.strip().split('==')[0].split('>=')[0].split('<=')[0].replace('-', '_')

def install_requirements():
    python_exec = f'"{sys.executable}"'
    with open("requirements.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pkg = pkg_name(line)
            if not is_installed(pkg):
                run(f"{python_exec} -m pip install {line}")
            else:
                print(f"Requirement already satisfied: {line}")

def main():
    python_exec = f'"{sys.executable}"'  # Quote the path

    # Upgrade pip
    run(f"{python_exec} -m pip install --upgrade pip")

    # Install requirements if not already installed
    install_requirements()

    # Run migrations
    os.chdir("battery_manager")
    run(f"{python_exec} manage.py migrate")

    # Collect static files
    run(f"{python_exec} manage.py collectstatic --noinput")

    # (Optional) Seed data
    # run(f"{python_exec} manage.py seed_data")

    # Run the ASGI server
    run(f"{python_exec} -m uvicorn battery_manager.asgi:application --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main()