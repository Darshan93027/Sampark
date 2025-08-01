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
├── auth_system                  ← App containing APIs for authentication JWT 
├── docs/
│    └── Sampark_postman_collection.json  ← Postman API collection
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

    git clone https://github.com/Darshan93027/Sampark.git
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
🧪 3. Django Setup Commands
============================

Run these commands inside the project folder:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Open your browser:
    http://127.0.0.1:8000/

============================
🚀 4. Workflow
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
📬 5. Postman API Collection
============================

For quick testing:

1. Open Postman
2. Import:
   - Sampark_postman_collection.json`
3. Use the collection to:
   - Sign up
   - Log in
   - Add SMTP credentials
   - Set OTP settings
   - Generate an API key
   - Send emails
   

============================
📦 6. Common Django Commands
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
