# Battery Manager Web Application

A Django-based web application for tracking battery replacements, maintenance, and reminders.

---

## Prerequisites

- **Python 3.10+** (recommended: Python 3.12)
- **Git** (optional, for cloning the repository)
- **pip** (Python package manager, comes with Python)
- **(Optional) Virtual Environment**: The setup script will create one if not present.

---

## Project Structure

```
battery_tracker/
│
├── battery_manager/         # Django project and app code
├── requirements.txt         # Python dependencies
├── setup_and_run.py         # Automated setup and run script
├── README.md                # This file
└── venv/                    # Virtual environment (created automatically)
```

---

## Setup & Running the Server

1. **Clone or Download the Project**

   ```
   git clone <your-repo-url>
   cd battery_tracker
   ```

2. **Run the Setup Script**

   The script will:
   - Create a virtual environment (if not present)
   - Prompt you to activate it (if not already active)
   - Install all requirements
   - Run migrations and collect static files
   - Ensure at least one superuser exists
   - Start the ASGI server

   **On Windows:**
   ```sh
   python setup_and_run.py
   ```

   If prompted, activate the virtual environment:
   ```
   venv\Scripts\activate
   ```

   Then re-run:
   ```
   python setup_and_run.py
   ```

3. **Access the Application**

   Open your browser and go to:  
   [http://localhost:8000](http://localhost:8000)

   - Admin interface: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Creating a Superuser

If no user exists, the script will prompt you to create a superuser (admin account) during setup.

---

## Additional Commands

- **Seed sample data:**  
  After setup, you can run:
  ```
  python battery_manager/manage.py seed_data
  ```

- **Run tests:**  
  ```
  python battery_manager/manage.py test
  ```

---

## Notes

- For production, configure `ALLOWED_HOSTS` and `DEBUG` in `battery_manager/settings.py`.
- Static files are collected to `staticfiles/`.
- For email reminders, configure email settings in `settings.py`.

---

## License

MIT License (or your chosen license)
