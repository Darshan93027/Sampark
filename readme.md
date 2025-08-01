===============================
📧 Sampark Mail API - Setup Guide
===============================

Sampark Mail API is a Django-based Email Automation & API service.
It provides:
✔ JWT-based user authentication
✔ Add custom SMTP credentials
✔ Send normal or OTP-based emails
✔ Configure OTP digit length (4/6/8)
✔ Generate API keys for external apps
✔ Log all sent/failed emails

This guide will help you:
✔ Setup virtual environment
✔ Configure .env file
✔ Migrate database
✔ Run Django project
✔ Use APIs via Postman

--------------------------------
📁 Project Folder Structure
--------------------------------

Sampark/
│
├── venv/                        ← Virtual environment folder
├── Sampark/                     ← Main Django configuration
├── mailapp/                     ← App containing APIs, models, utils
├── manage.py
├── requirements.txt
├── .env.example                 ← Example environment configuration
├── docs/
│    └── MailAPI.postman_collection.json  ← Postman API collection
├── README.md                    ← This file

============================
🧰 1. Requirements
============================

- Python 3.8 or newer
- pip
- Git
- Postman (for API testing)
- Gmail account (or SMTP provider)

============================
🐍 2. Virtual Environment Setup
============================

Clone the project:

    git clone https://github.com/yourusername/sampark.git
    cd sampark

Create and activate a virtual environment:

For Windows:
    python -m venv venv
    venv\Scripts\activate

For macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate

Install required dependencies:

    pip install -r requirements.txt

============================
🔐 3. Create and Configure .env
============================

Create a `.env` file in the root of the project.

# Django settings
SECRET_KEY=your_secret_key
DEBUG=True

# Default email settings (used by platform for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_official_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

These credentials are used by the platform itself.
Users will later provide their own credentials for sending emails through the API.

============================
🧪 4. Django Setup Commands
============================

Run these commands inside the project folder:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Open your browser:
    http://127.0.0.1:8000/

============================
🚀 5. Workflow
============================

Once the server is running:

1. Sign up a new user.
2. Log in to obtain JWT access/refresh tokens.
3. Add your SMTP credentials in the system (e.g., Gmail SMTP).
4. (Optional) Configure OTP settings (digit length and expiry time).
5. Generate an API key.
6. Use your API key to send:
   - Normal mails
   - OTP-based mails
7. For OTP mails, you can verify OTP using the OTP verification endpoint.
8. Mail logs (sent/failed) are stored in the database.

============================
📬 6. Postman API Collection
============================

For quick testing:

1. Open Postman
2. Import:
   - `docs/MailAPI.postman_collection.json`
3. Use the collection to:
   - Sign up
   - Log in
   - Add SMTP credentials
   - Set OTP settings
   - Generate an API key
   - Send emails
   - Verify OTP

============================
📦 7. Common Django Commands
============================

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    python manage.py createsuperuser

============================
👨‍💻 Author
============================

Darshan Sharma  
Email: contactdarshan07@gmail.com

============================
🎉 All Set!
============================
