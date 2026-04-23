# 🛒 Secure E-commerce Website with Vulnerability Testing

## 📌 Project Overview

This project is a secure e-commerce web application developed as part of a final-year computing and cybersecurity project. The system simulates a small online shopping platform where users can register, log in, browse products, add items to a cart, place orders, and manage their accounts.

The project focuses on secure development practices, user experience, and vulnerability mitigation, ensuring protection against common web security risks.

---

## 🚀 Features

### 👤 User Features
- User registration and login  
- Product catalogue with categories and search  
- Product detail page  
- Shopping cart (add, update, remove)  
- Auto cart quantity update (AJAX)  
- Checkout and order creation  
- Order history  
- Order cancellation  
- Email notifications (order confirmation & status updates)  

### 🛠 Admin Features
- Custom admin dashboard  
- Admin order management  
- Order status updates  
- Dashboard charts using Chart.js  
- Recent orders overview  
- Low stock product monitoring  

---

## 🔐 Security Features
- Authentication and authorization  
- Admin-only dashboard access  
- Input validation and sanitisation  
- Session protection  
- CSRF protection  
- Secure handling of sensitive data using environment variables  
- Prevention of invalid cart and order inputs  

---

## ⚡ Advanced Features
- Auto cart quantity update using AJAX (no page reload)  
- Real-time validation for cart and checkout  
- Responsive UI (mobile + desktop)  
- Improved user experience with dynamic updates  

---

## 📧 Email System

The application includes a working email system using Gmail SMTP:

- Order confirmation emails sent after checkout  
- Order status update emails from admin dashboard  
- Secure authentication using Gmail App Passwords  

---

## 🧰 Technology Stack
- Backend: Django (Python)  
- Frontend: HTML, CSS, Bootstrap  
- Database: SQLite  
- Charts: Chart.js  
- Version Control: Git & GitHub  
- Deployment: Render  

---

## ⚙️ Setup Instructions

### 1. Clone Repository

git clone <your-repo-link>
cd secure_ecommerce


### 2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Create `.env` File

SECRET_KEY=your_secret_key
EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_app_password


### 5. Run Migrations

python3 manage.py migrate


### 6. Create Superuser

python3 manage.py createsuperuser


### 7. Run Server

python3 manage.py runserver


---

## 📸 Screenshots

(Add screenshots here in GitHub or your report)

- Homepage  
- Product page  
- Cart page (auto update feature)  
- Checkout page  
- Order confirmation  
- Order history  
- Admin dashboard  

---

## 🎯 Project Status
- Completed  
- Fully functional  
- Secure implementation  
- Professional UI/UX  

---

## 👨‍💻 Author
Siddhartha Gupta  