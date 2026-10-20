# Full-Stack E-Commerce Web Application

**Internship Capstone Project | Auspify Technologies**  
*Built with Python, Django 5.2 LTS, Django REST Framework, MySQL, Bootstrap 5, and JavaScript (Fetch API).*

---

## 🌟 Project Overview

This is a production-grade, modular full-stack e-commerce web platform developed as an internship project for **Auspify Technologies**. It features a modern, responsive storefront powered by Bootstrap 5 and JavaScript Fetch API, backed by a Django 5.2 backend and MySQL database.

The application adheres to clean architecture principles with separate apps for Products, Users, Cart, and Orders, supported by both server-rendered Django templates and a documented RESTful API layer.

---

## 🛠 Technology Stack

- **Frontend:**
  - HTML5 & Modern CSS3
  - JavaScript (ES6+ with Fetch API)
  - Bootstrap 5.3 & Bootstrap Icons
- **Backend:**
  - Python 3.13+
  - Django 5.2 LTS
  - Django REST Framework (DRF)
  - django-filter & Pillow
- **Currency:** Indian Rupee (INR - ₹) across all storefront, cart, order receipts, and admin interfaces.
- **Database:**
  - MySQL 8.0+
  - mysqlclient & PyMySQL driver fallback

---

## 📁 Project Architecture & Directory Structure

```text
E-Commerce/
├── manage.py                     # Django project management script
├── requirements.txt              # Pinned python project dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore file for secrets and environments
├── README.md                     # Comprehensive project documentation
├── ecommerce/                    # Core configuration module
│   ├── __init__.py               # MySQLdb fallback bootstrap
│   ├── settings.py               # Django & DRF settings (MySQL configured)
│   ├── urls.py                   # Root URL routing & media serving
│   ├── api_urls.py               # Unified REST API router
│   ├── views.py                  # Custom error handlers (404)
│   ├── asgi.py
│   └── wsgi.py
├── products/                     # Product catalog & category management
│   ├── models.py                 # Category & Product models
│   ├── serializers.py            # Category & Product serializers
│   ├── views.py                  # Storefront & listing views
│   ├── api_views.py              # REST API endpoints with search & filter
│   ├── urls.py & api_urls.py
│   ├── admin.py                  # Admin configuration with image previews
│   └── management/commands/      # Custom load_sample_data command
├── users/                        # User registration, auth & profiles
│   ├── models.py                 # UserProfile model & automated signal
│   ├── serializers.py            # Registration, login & profile serializers
│   ├── views.py                  # HTML auth views
│   ├── api_views.py              # REST auth endpoints
│   ├── urls.py & api_urls.py
│   └── admin.py                  # Inlined user profile admin
├── cart/                         # Cart management & persistence
│   ├── models.py                 # Cart & CartItem models
│   ├── serializers.py            # Cart serialization & quantity validation
│   ├── views.py                  # Cart UI view
│   ├── api_views.py              # REST API for cart add, update, remove
│   ├── context_processors.py     # Global navbar cart counter
│   ├── urls.py & api_urls.py
│   └── admin.py
├── orders/                       # Checkout & order processing
│   ├── models.py                 # Order & OrderItem models
│   ├── serializers.py            # Order serializers & checkout validation
│   ├── views.py                  # Checkout, order list & invoice views
│   ├── api_views.py              # Atomic checkout & order retrieval
│   ├── urls.py & api_urls.py
│   └── admin.py                  # Status badges & order items inline
├── templates/                    # Clean HTML5 / Bootstrap 5 Templates
│   ├── base.html                 # Master layout with navbar, footer & toast
│   ├── navbar.html               # Global navbar with live badge & search
│   ├── footer.html               # Professional branded footer
│   ├── home.html                 # Hero, categories, and new arrivals
│   ├── products/
│   │   ├── product_list.html     # Catalog with search, filter & pagination
│   │   └── product_detail.html   # Product details, quantity selector & related
│   ├── users/
│   │   ├── register.html         # Sign-up page
│   │   ├── login.html            # Sign-in page
│   │   └── profile.html          # Profile & delivery address management
│   ├── cart/
│   │   └── cart.html             # Cart table with live Fetch API updates
│   ├── orders/
│   │   ├── checkout.html         # Checkout & Cash on Delivery
│   │   ├── order_list.html       # Past orders list
│   │   └── order_detail.html     # Order invoice confirmation
│   └── errors/
│       └── 404.html              # Custom 404 error page
├── static/
│   ├── css/styles.css            # Custom responsive styles & animations
│   ├── js/main.js                # ES6 Fetch API client & toasts
│   └── images/                   # Local assets & placeholder images
├── media/                        # User and product image uploads
└── tests/                        # Automated unit & integration tests
    ├── __init__.py
    └── test_ecommerce.py         # Full test suite (8 tests)
```

---

## ⚡ Quick Start Guide (Windows PowerShell)

Follow these exact steps to run the project locally.

### 1. Clone & Navigate to Project Directory
```powershell
cd e:\Auspfy_Internship\E-Commerce
```

### 2. Create and Activate Virtual Environment
```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell shows an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Create MySQL Database
Make sure your MySQL server is running. Open **MySQL 8.0 Command Line Client** or **MySQL Workbench** and execute:
```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure `.env`
Ensure your [.env](file:///.env) file exists with your MySQL credentials:
```env
SECRET_KEY=django-insecure-auspify-ecommerce-secret-key-2026-internship-project
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver

DB_ENGINE=django.db.backends.mysql
DB_NAME=ecommerce_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Run Migrations
Apply database migrations directly to MySQL:
```powershell
python manage.py migrate
```

### 7. Load Bundled Sample Products & Categories
Seed the database with sample categories, products, and generated bundled local assets:
```powershell
python manage.py load_sample_data
```

### 8. Create Administrator Superuser (Optional)
If not already created:
```powershell
python manage.py createsuperuser
```
*(Default development credentials: Username: `admin` | Password: `admin1234`)*

### 9. Start the Development Server
```powershell
python manage.py runserver
```
Visit **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser!

---

## 🌐 Pages & URLs Reference

| Page | URL Route | Description |
|---|---|---|
| **Home Page** | `http://127.0.0.1:8000/` | Hero banner, categories, new arrivals |
| **Product Catalog** | `http://127.0.0.1:8000/products/` | All products with filters and search |
| **Category Products** | `http://127.0.0.1:8000/category/<slug>/` | Filtered by specific category |
| **Product Details** | `http://127.0.0.1:8000/product/<slug>/` | Image, stock availability, add to cart |
| **Shopping Cart** | `http://127.0.0.1:8000/cart/` | Manage quantities and remove items |
| **Checkout** | `http://127.0.0.1:8000/orders/checkout/` | Enter delivery address, Cash on Delivery |
| **Order History** | `http://127.0.0.1:8000/orders/` | User past orders & status badges |
| **Order Invoice** | `http://127.0.0.1:8000/orders/<order_number>/` | Detailed order confirmation receipt |
| **Registration** | `http://127.0.0.1:8000/users/register/` | Create a new customer account |
| **Login** | `http://127.0.0.1:8000/users/login/` | Sign in to existing account |
| **User Profile** | `http://127.0.0.1:8000/users/profile/` | Edit personal and address details |
| **Django Admin** | `http://127.0.0.1:8000/admin/` | Management panel (admin / admin1234) |

---

## 📡 REST API Documentation

All endpoints return JSON and accept standard CSRF or session cookies for authenticated calls.

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/categories/` | List all categories with product counts | No |
| `GET` | `/api/products/` | Paginated product list with search, category & price filter | No |
| `GET` | `/api/products/<id>/` | Single product detail view | No |
| `POST` | `/api/auth/register/` | Register new user account | No |
| `POST` | `/api/auth/login/` | Authenticate user and initiate session | No |
| `POST` | `/api/auth/logout/` | Sign out user | Yes |
| `GET, PUT, PATCH` | `/api/auth/profile/` | View/update current user details and address | Yes |
| `GET` | `/api/cart/` | Retrieve authenticated user's cart | Yes |
| `POST` | `/api/cart/items/` | Add product to cart (body: `product_id`, `quantity`) | Yes |
| `PATCH` | `/api/cart/items/<id>/` | Update item quantity (body: `quantity`) | Yes |
| `DELETE` | `/api/cart/items/<id>/` | Remove item from cart | Yes |
| `POST` | `/api/orders/` | Place order / checkout within atomic transaction | Yes |
| `GET` | `/api/orders/` | List authenticated user's order history | Yes |
| `GET` | `/api/orders/<id>/` | Retrieve specific order detail | Yes |

---

## 🧪 Automated Testing

Run the comprehensive automated test suite with:

```powershell
python manage.py test tests
```

**Test Coverage Highlights:**
- `ProductAPITestCase`: Tests product list, keyword search, price range filter, and detail view.
- `UserAuthAPITestCase`: Tests registration, unique username/email constraints, login, profile retrieval, and logout.
- `CartAndOrderFlowTestCase`: Tests stock limit validation, live quantity updates, atomic order creation, server-side price calculation, safe inventory reduction, cart clearance, and cross-user order isolation.

---

## 🔧 Troubleshooting Common Errors

### 1. `django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'localhost'")`
- **Cause:** Incorrect MySQL root password.
- **Fix:** Update `DB_PASSWORD` in your `.env` file to match your MySQL password.

### 2. `django.db.utils.OperationalError: (1049, "Unknown database 'ecommerce_db'")`
- **Cause:** The database has not been created yet in MySQL.
- **Fix:** Connect to MySQL and run:
  ```sql
  CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### 3. `mysqlclient` C-compiler error on Windows
- **Fix:** `ecommerce/__init__.py` has been pre-configured with `PyMySQL` fallback. If `mysqlclient` encounters issues, `PyMySQL` automatically binds to MySQL transparently.

### 4. `django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header`
- **Fix:** Ensure `ALLOWED_HOSTS` in `.env` includes `127.0.0.1,localhost,testserver`.

---

## 📦 Git & GitHub Setup Instructions

To push this project to GitHub for your internship submission:

```powershell
# 1. Initialize Git repository
git init

# 2. Stage all files (.gitignore automatically protects .env and venv)
git add .

# 3. Create initial commit
git commit -m "feat: complete full-stack e-commerce project for Auspify Technologies internship"

# 4. Set default branch to main
git branch -M main

# 5. Add your remote GitHub repository URL
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 📸 Internship Submission Checklist

Before submitting your internship project:

1. **Take Screenshots:**
   - [ ] Home Page (`/`) with hero banner and categories
   - [ ] Product Catalog (`/products/`) with filters and search results
   - [ ] Product Detail Page (`/product/<slug>/`) showing stock badge and quantity controls
   - [ ] Shopping Cart (`/cart/`) showing items and order summary
   - [ ] Empty Cart state
   - [ ] Checkout Page (`/orders/checkout/`) with shipping details
   - [ ] Order Details / Receipt Page (`/orders/<order_number>/`)
   - [ ] User Profile Page (`/users/profile/`)
   - [ ] Django Admin Panel (`/admin/`) showing Products with thumbnails and Orders with colored status badges
   - [ ] MySQL Workbench showing the `ecommerce_db` tables
   - [ ] Terminal showing `python manage.py test tests` passing (8/8 tests OK)
2. **Repository Readiness:**
   - [ ] Verify `.env` is NOT committed (protected by `.gitignore`)
   - [ ] Verify `requirements.txt` is present
   - [ ] Verify `README.md` is complete
3. **Demo Video (Optional):**
   - Record a 2–3 minute screen walkthrough of user registration, browsing products, adding to cart, adjusting quantities, checking out with Cash on Delivery, and reviewing the order in both customer view and admin panel.
