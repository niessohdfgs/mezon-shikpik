# Tailoring Academy Backend

## Overview

Tailoring Academy Backend is a RESTful API backend for an online tailoring education platform.

The project provides a complete backend system for managing online courses, educational content, digital patterns, users, purchases, orders, payments, discounts, and protected user access.

The backend is designed with a modular architecture using Django applications, where each business domain is separated into independent modules.

The frontend application is developed separately using **Next.js** and communicates with this backend through REST APIs.

---

# Project Goals

The main purpose of this backend is to provide a secure and scalable platform where users can:

- Register and authenticate
- Browse available courses
- Purchase educational content
- Watch purchased lessons
- Track learning progress
- Download purchased tailoring patterns
- Manage their orders and purchases

Administrators can:

- Manage users
- Manage courses
- Manage lessons
- Manage patterns
- Manage products
- Manage orders
- Manage discounts
- View system analytics

---

# Technology Stack

## Backend

- Python 3.11
- Django 5.2
- Django REST Framework

## Database

- PostgreSQL 15

## Authentication

- JWT Authentication
- Custom Django User Model
- Token based authentication

## Background Processing

- Redis
- Celery

## API Documentation

- drf-spectacular
- OpenAPI Schema
- Swagger UI

## Deployment

- Docker
- Docker Compose
- Gunicorn
- Nginx

---

# Architecture Overview

The backend follows a layered architecture:


Client
|
|
REST API
|
|
Django REST Framework
|
|
Business Logic Services
|
|
Database Layer
(PostgreSQL)


Business logic is separated from views using service classes where necessary.

Examples:


commerce/services/

order.py
discount.py
access.py
zarinpal.py

This keeps views simple and makes the system easier to maintain and extend.

---

# Backend Structure

Main project structure:


backend/

├── accounts/
│
├── courses/
│
├── patterns/
│
├── commerce/
│
├── adminpanel/
│
├── config/
│
├── media/
│
├── staticfiles/
│
├── manage.py
│
├── requirements.txt
│
└── Dockerfile


---

# Django Applications

The backend is divided into several Django apps.

Each application has a specific responsibility.

---

# accounts

Responsible for all user-related functionality.

Main responsibilities:

- Custom user model
- Authentication
- OTP system
- User sessions
- User permissions
- Profile management
- User blocking

Main models:


User

OTPCode

UserSession


The project uses a custom user model:


AUTH_USER_MODEL = "accounts.User"


instead of Django's default authentication model.

---

# courses

Responsible for educational content management.

The application handles:

- Courses
- Chapters
- Lessons
- Lesson progress
- Continue watching functionality

Course structure:


Course

└── Chapter

  └── Lesson

Main models:


Course

Chapter

Lesson

LessonProgress

CoursePurchase


Only published content is visible publicly.

Private educational content requires ownership verification.

---

# patterns

Responsible for digital tailoring patterns.

Features:

- Pattern management
- Pattern publishing
- Pattern information
- Protected pattern downloads

Main model:


Pattern


Pattern files are protected and users can only download purchased patterns.

---

# commerce

The commerce application handles all purchasing functionality.

Responsibilities:

- Products
- Shopping cart
- Orders
- Purchases
- Payments
- Discounts
- Wishlist

Main models:


Product

Cart

CartItem

Order

OrderItem

Purchase

Payment

Discount

Wishlist


---

# adminpanel

Provides custom administration APIs.

The admin panel handles:

- Dashboard information
- User management
- Product analytics
- Sales analytics
- System statistics

The project does not rely only on Django default admin.

Custom APIs are provided for frontend administration if needed.


adminpanel/


---

# Configuration

Main Django configuration:


config/


Contains:


settings.py

urls.py

wsgi.py

celery.py


The project uses:

- Environment based configuration
- PostgreSQL connection
- Redis cache
- Celery worker configuration
- REST Framework settings
# Authentication System

## Overview

The authentication system is implemented using a custom Django User model.

The project does not use Django's default User model.

Instead, it uses:


accounts.User


This allows the system to support phone-based authentication and future extensions.

---

# Authentication Features

The authentication module supports:

- User registration
- User login
- JWT token authentication
- Refresh token mechanism
- OTP verification infrastructure
- User sessions
- Logout current session
- Logout all sessions
- User blocking system
- Role management

---

# JWT Authentication

The API authentication is based on JSON Web Tokens.

The backend uses:


djangorestframework-simplejwt


Authentication flow:


User Login

 |

Backend validates credentials

 |

Generate JWT Access Token

 |

Generate JWT Refresh Token

 |

Client stores tokens

 |

Client sends Access Token with requests


Authenticated requests require:


Authorization: Bearer <access_token>


---

# Token Configuration

Current configuration:

```python
ACCESS_TOKEN_LIFETIME = 7 days

REFRESH_TOKEN_LIFETIME = 30 days

Access tokens are short-lived and refresh tokens are used to obtain new access tokens.

OTP System

The project contains OTP infrastructure for mobile verification.

OTP responsibilities:

Mobile number verification
Registration verification
Future passwordless authentication support

Main model:

OTPCode

OTP workflow:

User enters phone number

        |

Backend generates OTP

        |

OTP is sent through SMS service

        |

User submits OTP

        |

Backend verifies OTP

        |

Account becomes verified
Session Management

The project contains a custom session system.

Main model:

UserSession

Responsibilities:

Tracking user sessions
Managing active sessions
Logout from specific sessions
Logout from all devices
User Permissions

The system supports different user permissions.

Examples:

Normal user
Admin user

Admin access is controlled using:

accounts.permissions.IsAdmin

Protected endpoints require:

IsAuthenticated

+

IsAdmin
Course Access Control
Overview

Paid educational content is protected using ownership verification.

Users can only access purchased courses.

The access logic is centralized in:

commerce/services/access.py
Access Service

Main service:

AccessService

Important methods:

has_course_access(
    user,
    course
)

Checks whether a user owns a course.

has_pattern_access(
    user,
    pattern
)

Checks whether a user owns a pattern.

Course Access Rules
Free Courses

Free courses are available without purchase.

Example:

Course.is_free = True

Access:

User
 |
 |
Free Course
 |
 |
Allowed
Paid Courses

Paid courses require purchase ownership.

Flow:

User requests lesson

        |

Backend finds course

        |

Check Purchase table

        |

Purchase exists?

        |

YES  -> Allow access

NO   -> Return 403 Forbidden
Protected Course Content

Protected endpoints:

Course Content API

Lesson Detail API

Lesson Stream API

Lesson Progress API

Before returning content, the backend verifies ownership.

Lesson Video Protection

Lesson videos are not publicly exposed through direct URLs.

The backend checks:

User authentication
Lesson existence
Course ownership

Only after successful validation the video resource is returned.

Pattern Security
Overview

Digital tailoring patterns are protected downloadable files.

Users cannot download patterns without purchase ownership.

Pattern Download Flow
User requests pattern download

          |

Authentication check

          |

Find pattern

          |

Check Purchase ownership

          |

Permission granted

          |

Return protected file
Pattern Access Validation

Implemented in:

commerce/services/access.py

Method:

has_pattern_access(
    user,
    pattern
)
Commerce System

The commerce system manages all purchase-related operations.

Main responsibilities:

Product management
Cart management
Checkout
Orders
Purchases
Payments
Discounts
Wishlist
Product System

Courses and patterns are represented as products.

Product types:

Course Product

Pattern Product

Each product contains:

title

type

price

course

pattern

is_active
Purchase Rules

Business rules:

Each product can only be purchased once by each user
Purchased access is permanent
Admin can revoke access if required
Users cannot purchase inactive products
Shopping Cart

Cart functionality includes:

Add products
Remove products
Update quantity
Apply discount
Calculate final price

Main models:

Cart

CartItem
Order System

Orders represent checkout operations.

Order flow:

Cart

 |

Checkout

 |

Create Order

 |

Create Payment

 |

Verify Payment

 |

Create Purchase

Main models:

Order

OrderItem
Checkout Process

Checkout endpoint:

POST /api/checkout/

Process:

Validate cart
Validate products
Apply discount
Create order
Create payment request
Redirect to payment gateway
# Payment System

## Overview

The payment system is designed to handle online purchases through a payment gateway.

The current implementation is prepared for Zarinpal integration.

Payment responsibilities:

- Create payment request
- Redirect user to gateway
- Verify payment result
- Store payment information
- Create purchase after successful payment

---

# Payment Flow

The payment process:


User Checkout

    |

Order Created

    |

Payment Created

    |

Request Payment Gateway

    |

User Completes Payment

    |

Gateway Callback

    |

Payment Verification

    |

Purchase Created


---

# Payment Model

Main model:


Payment


Stores:

- Payment amount
- Payment status
- Gateway authority
- Reference ID
- Creation time

Example statuses:


pending

paid

failed


---

# Zarinpal Integration

Payment service location:


commerce/services/zarinpal.py


Responsibilities:

- Create payment request
- Generate payment URL
- Verify transaction

Environment variables:

```env
ZARINPAL_MERCHANT_ID=

ZARINPAL_CALLBACK_URL=
Discount System

The discount system allows users to apply discount codes before checkout.

Features:

Discount validation
Percentage discounts
Expiration checking
Active/inactive discounts

Main model:

Discount
Discount Flow
User enters discount code

          |

Backend validates code

          |

Check expiration

          |

Check active status

          |

Apply discount

          |

Calculate final price
Background Tasks

The backend uses Celery for asynchronous tasks.

Technology:

Celery

+

Redis

Configuration:

config/celery.py

Possible future tasks:

Sending SMS notifications
Email notifications
Payment notifications
Background processing
Redis Usage

Redis is used for:

Celery message broker
Cache management

Configuration:

CELERY_BROKER_URL =
"redis://redis:6379/0"

Cache backend:

django_redis
Docker Setup

The backend is fully containerized.

Services:

backend

nginx

postgres

redis

celery
Docker Compose Architecture
                Client

                  |

                Nginx

                  |

              Gunicorn

                  |

              Django API

                  |

        --------------------

        |                  |

    PostgreSQL          Redis

                          |

                       Celery
Running The Project
Requirements

Install:

Docker
Docker Compose
Environment Configuration

Create:

backend/.env

Example:

SECRET_KEY=your-secret-key

DEBUG=True


POSTGRES_DB=tailoring

POSTGRES_USER=postgres

POSTGRES_PASSWORD=password

POSTGRES_HOST=tailoring_postgres

POSTGRES_PORT=5432


ZARINPAL_MERCHANT_ID=

ZARINPAL_CALLBACK_URL=

Never commit .env files.

Start Project

Build containers:

docker compose build

Run services:

docker compose up -d

Check services:

docker compose ps
Useful Django Commands
Django Check
docker exec -it tailoring_backend python manage.py check
Apply Migrations
docker exec -it tailoring_backend python manage.py migrate
Create Migrations
docker exec -it tailoring_backend python manage.py makemigrations
Generate API Schema
docker exec -it tailoring_backend python manage.py spectacular --file schema.yml
API Documentation

The project uses OpenAPI documentation.

Generated file:

schema.yml

Swagger endpoint:

/api/docs/

Schema endpoint:

/api/schema/
Database Management

The project uses PostgreSQL.

Database container:

tailoring_postgres

Database:

tailoring
Backup Database

Create backup:

docker exec -t tailoring_postgres pg_dump -U postgres tailoring > backup.sql

Restore backup:

Linux:

docker exec -i tailoring_postgres psql -U postgres tailoring < backup.sql

PowerShell:

Get-Content backup.sql | docker exec -i tailoring_postgres psql -U postgres -d tailoring
Migration Testing

Check migration status:

docker exec -it tailoring_backend python manage.py showmigrations

Check pending migrations:

docker exec -it tailoring_backend python manage.py migrate --plan
Security Notes

The backend includes multiple security layers.

Authentication Protection

Private APIs require:

JWT Authentication
Content Protection

Paid content is protected using purchase verification.

Protected resources:

Course content
Lessons
Video streams
Pattern files
Media Protection

User uploaded files are not considered public resources.

Access should always be validated before returning protected files.

Environment Security

Sensitive information should never be committed:

.env

database backups

secret keys
Performance Optimization

Implemented optimizations:

select_related for related objects
prefetch_related for collections
Query optimization
Pagination support

Examples:

select_related(
    "payment"
)

prefetch_related(
    "items"
)
Project Development Workflow

Recommended workflow:

Create Feature Branch

        |

Develop Feature

        |

Run Tests

        |

Run Django Check

        |

Commit Changes

        |

Push Branch

        |

Create Pull Request

        |

Review & Merge
Current Project Status

Completed:

✅ Docker setup
✅ PostgreSQL integration
✅ Redis integration
✅ Celery configuration
✅ JWT authentication
✅ Course management
✅ Lesson protection
✅ Pattern protection
✅ Commerce system
✅ Cart system
✅ Order system
✅ Discount system
✅ Payment infrastructure
✅ Admin APIs
✅ API documentation
✅ Database backup workflow

Contact Information

Developer:

Name: hossein seyedzadeh

Email: hosseinseyedzadeh93@gmail.com

GitHub:github.com/niessohdfgs

GitHub Profile:niessohdfgs

