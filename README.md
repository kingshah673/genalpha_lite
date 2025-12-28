# GenAlpha - Premium Clothing E-Commerce

**GenAlpha** is a fully functional, premium clothing e-commerce web application built with **Django** (Backend) and **Tailwind CSS** (Frontend). It features a modern, responsive design, a session-based cart with HTMX-powered updates, a comprehensive admin dashboard, and a robust PostgreSQL database integration.

---

## 🚀 Key Features

### 🛒 Customer Experience
-   **Premium UI/UX**: Responsive design with smooth scrolling, glassmorphism effects, fade-in animations, and a rich dark/light aesthetic.
-   **Dynamic Homepage**:
    -   Hero banner slider with "Shop Now" CTAs.
    -   Featured Categories grid.
    -   "New Arrivals" and "Best Sellers" showcased products.
    -   Brand Story section.
-   **Product Catalog**:
    -   Shop page with sidebar filtering (Category) and sorting options.
    -   Product searching and pagination.
    -   Product Detail Page: Image gallery, size/color variant selection, real-time stock availability check.
-   **Smart Cart System**:
    -   **Session-based**: Persists for anonymous users.
    -   **Slide-out Drawer**: View and manage cart items instantly without leaving the page (powered by HTMX).
    -   **Full Cart Page**: Detailed view with quantity updates and removal options.
-   **Checkout Flow**:
    -   Guest checkout supported.
    -   Shipping confirmation and Order Summary.
    -   Real-time form validation with error messages.

### 🛠️ Admin & Management
-   **Dashboard**: Manage Products, Categories, Orders, and Hero Banners.
-   **Inventory Control**: Track stock for individual size/color variants.
-   **Order processing**: View customer details, update order status (Pending, Shipped, Delivered).
-   **Media Management**: Upload and manage product and category images (max 5MB validation).

### ⚙️ Technical Highlights
-   **Backend**: Django 5.x, Python 3.12.
-   **Database**: PostgreSQL (v18 confirmed, v15+ supported).
-   **Frontend**: Tailwind CSS (CDN for dev, CLI ready), Alpine.js (interactivity), HTMX (AJAX-like updates).
-   **SEO & Performance**:
    -   Dynamic Meta Tags & Open Graph support.
    -   Lazy loading for images.
    -   Sitemaps (`sitemap.xml`) and `robots.txt` generation.
-   **Security**:
    -   CSRF Protection.
    -   Input sanitization.
    -   Secure environment variable management (`python-dotenv`).

---

## 🛠️ Installation & Setup

### Prerequisites
-   Python 3.10+
-   PostgreSQL 15+ (Verified on v18)

### 1. Clone & Environment
```bash
# Clone the repository (if applicable) or verify project root
cd brandstore

# Create Virtual Environment
python -m venv .venv

# Activate Virtual Environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
1.  Copy the example env file:
    ```bash
    copy .env.example .env
    ```
2.  Open `.env` and configure your database settings.
    > **Note:** Check your PostgreSQL port! Default is `5432`, but if you have multiple versions, it might be `5433`.
    ```ini
    # Example .env configuration
    DEBUG=True
    SECRET_KEY=your-secret-key
    ALLOWED_HOSTS=127.0.0.1,localhost
    DATABASE_URL=postgres://postgres:1234@localhost:5433/genalpha_lite
    ```

### 4. Database Setup
Ensure your PostgreSQL server is running and the database exists (or create it):
```bash
# Apply Migrations
python manage.py migrate
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
# Follow the prompts to set username (e.g., admin) and password
```

### 6. Run Server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ to browse the site.

---

## 📖 Usage Guide

### Logging into Admin
-   Navigate to `http://127.0.0.1:8000/admin/`
-   Log in with your superuser credentials.
-   **Tip**: Start by creating a few **Categories** and **Products** to populate the homepage.

### Verifying Features
1.  **Add to Cart**: Go to any product, select a Size/Color, and click "Add to Cart". The drawer should slide out.
2.  **Checkout**: Proceed to checkout, fill in dummy shipping info, and confirm the order.
3.  **Check Order**: Go back to the Admin panel > **Orders** to see the new transaction.

---

## 📂 Project Structure

```text
brandstore/
├── brandstore/         # Project configuration (settings, urls, wsgi)
├── core/               # Homepage, Banners, About/Contact pages
├── products/           # Product models, views, and catalog logic
├── cart/               # Cart session management and HTMX views
├── orders/             # Order processing and checkout logic
├── templates/          # HTML Templates (Tailwind + Alpine.js)
├── static/             # CSS, JS, images
├── media/              # User-uploaded content (Products, Banners)
├── .env                # Environment variables (IGNORED in git)
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

---

*Verified and Tested on Windows 11 with PostgreSQL 18.*
