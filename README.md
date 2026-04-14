# Coderr Backend API

A comprehensive Django REST API backend for the Coderr platform - a marketplace connecting customers with business service providers. This API enables user authentication, profile management, service offers, order processing, and review functionality.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Admin Panel](#admin-panel)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Models](#models)
- [Testing](#testing)
- [Development Notes](#development-notes)

## ✨ Features

### User Management
- **User Registration & Authentication** - Token-based authentication system
- **Dual Profile Types** - Customer and Business user profiles
- **Profile Management** - Complete CRUD operations for user profiles
- **Profile Pictures** - File upload support for profile images

### Service Marketplace
- **Service Offers** - Businesses can create and manage service offers
- **Offer Details** - Multiple pricing tiers (Basic, Standard, Premium)
- **Flexible Pricing** - Custom pricing, revisions, and delivery times
- **Image Support** - Upload images for service offers

### Order System
- **Order Creation** - Customers can purchase service offers
- **Order Tracking** - Track order status (In Progress, Completed, Cancelled)
- **Order Management** - Full CRUD operations for orders
- **Business Analytics** - Order count and completion statistics per business

### Review System
- **Rating & Reviews** - 5-star rating system with text reviews
- **Review Management** - Create, update, and delete reviews
- **Business Reputation** - One review per customer per business

### Base Information
- **Platform Statistics** - Access to platform-wide statistics and information

## 🛠 Tech Stack

- **Framework:** Django 6.0.1
- **API:** Django REST Framework 3.16.1
- **Database:** PostgreSQL
- **Server:** Gunicorn (via Docker)
- **Containerization:** Docker & Docker Compose
- **Authentication:** Token Authentication (DRF)
- **Image Processing:** Pillow 12.1.0
- **CORS:** django-cors-headers 4.9.0
- **Filtering:** django-filter 25.2
- **Python Version:** 3.12 (Alpine)

## 📁 Project Structure

```
coderr.backend/
├── auth_app/              # Authentication (Login, Registration, Logout)
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── tests/
├── profiles_app/          # User Profiles (Customer & Business)
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── tests/
├── offers_app/            # Service Offers & Details
│   ├── api/
│   │   ├── filters.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── tests/
├── orders_app/            # Order Management
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── tests/
├── reviews_app/           # Rating & Review System
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── tests/
├── base_info_app/         # Platform Statistics
│   └── api/
├── core/                  # Django Project Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                 # User uploaded files
├── backend.Dockerfile
├── backend.entrypoint.sh
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## 🚀 Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/b-rich-dev/coderr.backend
   cd coderr.backend
   ```

2. **Create a `.env` file** in the project root with the following variables:
   ```env
   # Django
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
   CSRF_TRUSTED_ORIGINS=http://localhost:8000

   # Database
   DB_NAME=coderr_db
   DB_USER=coderr_user
   DB_PASSWORD=supersecretpassword
   DB_HOST=db
   DB_PORT=5432

   # Superuser (auto-created on first start)
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=adminpassword
   ```

3. **Build and start the containers**
   ```bash
   docker compose up --build
   ```

The API will be available at `http://127.0.0.1:8000/`

> **Note:** On first startup, the entrypoint automatically runs `migrate`, `collectstatic`, and creates the superuser and demo guest accounts (`andrey` / `kevin`).

### Useful Docker Commands

```bash
# Start in detached mode
docker compose up -d

# Stop containers
docker compose down

# View logs
docker compose logs -f web

# Run management commands inside the container
docker compose exec web python manage.py <command>

# Run tests
docker compose exec web python manage.py test
```

## 🗝️ Admin Panel

Django Admin is fully configured for managing all platform data.

### Access Admin Panel

1. **Superuser is created automatically** on first container start using the environment variables:
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

2. **Access the admin interface**
   ```
   http://127.0.0.1:8000/admin/
   ```

3. **Login** with your superuser credentials

### Available Admin Sections

#### **Profiles Management**
- View all user profiles (Customer & Business)
- Filter by profile type and creation date
- Search by username, email, location
- Edit profile information and upload files

#### **Offers Management**
- Manage all service offers
- **Inline editing** of offer details (Basic, Standard, Premium)
- View offer creator and timestamps
- Search by title, description, or creator
- Filter by creation/update date

#### **Orders Management**
- Monitor all platform orders
- View customer and business information
- Track order status (In Progress, Completed, Cancelled)
- Filter by status, offer type, and date
- Search by title, customer, or business username
- **Note:** Order snapshot data is readonly after creation

#### **Reviews Management**
- View all customer reviews
- Filter by rating (1.0-5.0) and date
- Search by business, reviewer, or description
- Manage review content and ratings

#### **User Management**
- Django's built-in user management
- Create, edit, and delete users
- Manage permissions and groups

### Admin Features

✅ **List Views** - Sortable columns with pagination
✅ **Advanced Filtering** - Filter by status, type, date, etc.
✅ **Search Functionality** - Quick search across relevant fields
✅ **Bulk Actions** - Delete multiple items at once
✅ **Inline Editing** - Edit related models without leaving the page
✅ **Readonly Fields** - Protected fields like timestamps and snapshots
✅ **Fieldsets** - Organized form sections for better UX

## �🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/login/` | Login and receive auth token | No |
| POST | `/api/logout/` | Logout and invalidate token | Yes |

**Registration Request Body:**
```json
{
  "username": "exampleUsername",
  "email": "example@mail.de",
  "password": "examplePassword",
  "repeated_password": "examplePassword",
  "type": "customer"
}
```

**Login Request Body:**
```json
{
  "username": "exampleUsername",
  "password": "examplePassword"
}
```

**Login Response:**
```json
{
  "token": "83bf098723b08f7b23429u0fv8274",
  "username": "exampleUsername",
  "email": "example@mail.de",
  "user_id": 123
}
```

### Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profile/<id>/` | Get profile details | Yes |
| PUT | `/api/profile/<id>/` | Update profile | Yes |
| PATCH | `/api/profile/<id>/` | Partial update profile | Yes |
| POST | `/api/upload/` | Upload profile picture | Yes |
| GET | `/api/profiles/business/` | List all business profiles | Yes |
| GET | `/api/profiles/customer/` | List all customer profiles | Yes |

**Profile Response (GET/PUT/PATCH `/api/profile/<id>/`):**
```json
{
  "user": 1,
  "username": "max_mustermann",
  "first_name": "Max",
  "last_name": "Mustermann",
  "file": "profile_picture.jpg",
  "location": "Berlin",
  "tel": "123456789",
  "description": "Business description",
  "working_hours": "9-17",
  "type": "business",
  "email": "max@business.de",
  "created_at": "2023-01-01T12:00:00Z"
}
```

### Offers Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/offers/` | List all offers | Yes |
| POST | `/api/offers/` | Create new offer | Yes (Business) |
| GET | `/api/offers/<id>/` | Get offer details | Yes |
| PUT | `/api/offers/<id>/` | Update offer | Yes (Owner) |
| PATCH | `/api/offers/<id>/` | Partial update offer | Yes (Owner) |
| DELETE | `/api/offers/<id>/` | Delete offer | Yes (Owner) |
| GET | `/api/offerdetails/<id>/` | Get specific offer detail | Yes |

**Offer Response (GET `/api/offers/` or GET `/api/offers/<id>/`):**
```json
{
  "id": 1,
  "user": 1,
  "title": "Website Design",
  "image": null,
  "description": "Professionelles Website-Design...",
  "created_at": "2024-09-25T10:00:00Z",
  "updated_at": "2024-09-28T12:00:00Z",
  "details": [
    {
      "id": 1,
      "url": "/offerdetails/1/"
    },
    {
      "id": 2,
      "url": "/offerdetails/2/"
    },
    {
      "id": 3,
      "url": "/offerdetails/3/"
    }
  ],
  "min_price": 100,
  "min_delivery_time": 7,
  "user_details": {
    "first_name": "John",
    "last_name": "Doe",
    "username": "jdoe"
  }
}
```

**Offer Detail Response (GET `/api/offerdetails/<id>/`):**
```json
{
  "id": 1,
  "title": "Basic Package",
  "revisions": 2,
  "delivery_time_in_days": 7,
  "price": "100.00",
  "features": ["Feature 1", "Feature 2"],
  "offer_type": "basic"
}
```

### Orders Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List user's orders | Yes |
| POST | `/api/orders/` | Create new order | Yes (Customer) |
| GET | `/api/orders/<id>/` | Get order details | Yes (Owner) |
| PUT | `/api/orders/<id>/` | Update order | Yes (Owner) |
| PATCH | `/api/orders/<id>/` | Partial update order | Yes (Owner) |
| DELETE | `/api/orders/<id>/` | Delete order | Yes (Owner) |
| GET | `/api/order-count/<business_user_id>/` | Get order count for business | Yes |
| GET | `/api/completed-order-count/<business_user_id>/` | Get completed order count | Yes |

**Order Response (GET/POST/PUT/PATCH `/api/orders/` or `/api/orders/<id>/`):**
```json
{
  "id": 1,
  "customer_user": 2,
  "business_user": 5,
  "title": "Basic Package",
  "revisions": 2,
  "delivery_time_in_days": 7,
  "price": "100.00",
  "features": ["Feature 1", "Feature 2"],
  "offer_type": "basic",
  "status": "in_progress",
  "created_at": "2024-09-25T10:00:00Z",
  "updated_at": "2024-09-28T12:00:00Z"
}
```

**Order Create Request (POST `/api/orders/`):**
```json
{
  "offer_detail_id": 1
}
```

**Order Update Request (PUT/PATCH `/api/orders/<id>/`):**
```json
{
  "status": "completed"
}
```

### Reviews Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/reviews/` | List reviews | Yes |
| POST | `/api/reviews/` | Create review | Yes (Customer) |
| GET | `/api/reviews/<id>/` | Get review details | Yes |
| PUT | `/api/reviews/<id>/` | Update review | Yes (Owner) |
| PATCH | `/api/reviews/<id>/` | Partial update review | Yes (Owner) |
| DELETE | `/api/reviews/<id>/` | Delete review | Yes (Owner) |

**Review Response (GET/POST/PUT/PATCH `/api/reviews/` or `/api/reviews/<id>/`):**
```json
{
  "id": 1,
  "business_user": 5,
  "reviewer": 2,
  "rating": "4.5",
  "description": "Excellent service!",
  "created_at": "2024-09-25T10:00:00Z",
  "updated_at": "2024-09-28T12:00:00Z"
}
```

**Review Create/Update Request (POST/PUT/PATCH):**
```json
{
  "business_user": 5,
  "rating": "4.5",
  "description": "Excellent service!"
}
```

### Base Info Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/base-info/` | Get platform statistics | Yes |

**Base Info Response:**
```json
{
  "review_count": 150,
  "average_rating": 4.3,
  "business_profile_count": 25,
  "offer_count": 75
}
```

## 🔐 Authentication

This API uses **Token Authentication**. After successful login, include the token in all subsequent requests.

### Request Headers

```http
Authorization: Token <your-token-here>
```

### Example with cURL

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://127.0.0.1:8000/api/profile/1/
```

### Example with JavaScript

```javascript
fetch('http://127.0.0.1:8000/api/profile/1/', {
  headers: {
    'Authorization': 'Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b',
    'Content-Type': 'application/json'
  }
})
```

## 📊 Models

### User Profile Types

- **Customer** - Can browse offers, place orders, and submit reviews
- **Business** - Can create offers, receive orders, and get reviewed

### Key Relationships

```
User (Django Auth)
  └── Profile (OneToOne)
      ├── Offers (ForeignKey) - if type='business'
      │   └── OfferDetails (ForeignKey)
      │       └── Orders (ForeignKey)
      ├── Reviews as Reviewer (ForeignKey)
      └── Reviews as Business (ForeignKey)
```

## 🧪 Testing

Run the test suite inside the running container:

```bash
# Run all tests
docker compose exec web python manage.py test

# Run tests for specific app
docker compose exec web python manage.py test auth_app
docker compose exec web python manage.py test profiles_app
docker compose exec web python manage.py test offers_app
docker compose exec web python manage.py test orders_app
docker compose exec web python manage.py test reviews_app
```

### Test Coverage

- ✅ Authentication (Registration, Login, Logout)
- ✅ Profile Management
- ✅ Offer CRUD Operations
- ✅ Offer Details Management
- ✅ Order Creation and Management
- ✅ Order Statistics
- ✅ Review System
- ✅ Base Info Endpoints

## 🔧 Development Notes

### CORS Configuration

Configured for local development with frontend running on:
- `http://127.0.0.1:5500`
- `http://localhost:5500`

Update [core/settings.py](core/settings.py) for production deployments.

### Media Files

Uploaded files (profile pictures, offer images) are stored in:
```
media/
├── profile_pictures/
└── offer_images/
```

### Code Documentation

- All code documentation is in **English**
- Classes are documented.

### Permissions

- Default: All endpoints require authentication
- Custom permissions implemented for:
  - Offer creation (Business users only)
  - Order creation (Customer users only)
  - Owner-only modifications

## 📝 Environment Variables

All configuration is done via the `.env` file. See the [Installation](#installation) section for a full template.

| Variable | Description | Default |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | insecure dev key |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins | *(empty)* |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated CSRF origins | *(empty)* |
| `DB_NAME` | PostgreSQL database name | `coderr_db` |
| `DB_USER` | PostgreSQL user | `coderr_user` |
| `DB_PASSWORD` | PostgreSQL password | — |
| `DB_HOST` | PostgreSQL host (Docker service name) | `db` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DJANGO_SUPERUSER_USERNAME` | Auto-created superuser name | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Auto-created superuser email | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD` | Auto-created superuser password | `adminpassword` |

## 👥 User Types

| Type | Capabilities |
|------|--------------|
| **Customer** | Browse offers, place orders, write reviews |
| **Business** | Create offers, receive orders, get reviewed |

## 🤝 Contributing

This is a learning project. Feel free to:
1. Clone the repository

## 📄 License

This project is part of the Developer Akademie backend coursework.

## 📧 Contact

For questions or feedback regarding this project, please contact me or the Developer Akademie.

---

**Built with ❤️ using Django REST Framework**
