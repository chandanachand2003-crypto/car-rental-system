Car Rental System
A full-featured web-based Car Rental Management System built using Flask and MongoDB.

🚗 Project Overview
This app allows users to browse, book, and manage car rentals easily, while providing managers with secure controls for car addition, editing, deletion, and booking oversight.

🔐 Manager Login
Manager login page: /manager/login

Default manager credentials:

Username: manager

Password: manager123

These defaults can be changed using environment variables:

bash
set MANAGER_USER=manager
set MANAGER_PASS=manager123
👤 User Features
Register and log in as a user

Browse available cars

Filter cars by brand, seats, fuel type, rent, etc.

Book cars for a custom duration, with optional driver

View and manage your bookings (see receipts, cancel future bookings)

Secure password storage and validation

Logout anytime

🛠️ Manager Features
Secure login for managers

Dashboard overview of all cars and bookings

Add new cars with image upload (only PNG, JPG, JPEG, GIF; max 5MB)

Edit car details and images

Soft-delete cars (hidden from users, not deleted from DB)

View active bookings/rentals for each car

Logout anytime

🏗️ Tech Stack
Backend: Python Flask

Database: MongoDB

Frontend: HTML, CSS (Bootstrap), custom templates

File uploads: Managed and validated locally

⚡ Running the Project Locally
Install dependencies

bash
pip install -r requirements.txt
Start MongoDB locally (default: mongodb://localhost:27017/car_rental).

Set secrets/environment variables (strongly recommended for production):

bash
set SECRET_KEY=your_long_random_secret
set MONGO_URI=mongodb://localhost:27017/car_rental
set MANAGER_USER=manager
set MANAGER_PASS=manager123
Run the app

bash
python app.py
Visit in your browser:

text
http://127.0.0.1:5000/
📦 Project Structure
text
├── app.py                   # Main Flask app
├── requirements.txt         # Python dependencies
├── static/                  # CSS, JS, static images
├── uploads/                 # Uploaded car images
├── templates/               # HTML templates
├── .gitignore
└── README.md
⚙️ Advanced/Production Notes
All session and password secrets are managed using environment variables

Uploaded files are validated for type (image only) and size

Use Gunicorn or Waitress for production WSGI server

Manager credentials can be set in environment rather than code

✨ Features List
User authentication (register/login/logout)

Manager authentication (secure login/logout)

Car search and filters

Car booking and rental management

Soft delete for car records

Image upload with validation (PNG, JPG, JPEG, GIF, max 5MB)

Secure password hashing for users

Booking receipt and summary

Manager dashboard for bookings and car management

Environment-based secrets (never hardcoded!)

🗝 Security Highlights
No hardcoded secrets or passwords (everything via environment)

Session, cookie, and upload protection enabled

All dependencies clearly listed (requirements.txt)

SOFT DELETE logic to prevent accidental data loss