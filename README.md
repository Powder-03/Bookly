# 📚 Bookly - Book Management API

A modern FastAPI-based REST API for managing books, users, reviews, and tags with full authentication and role-based access control.

## 🚀 Features

- **User Management**: Registration, login, email verification, password reset
- **Book Management**: CRUD operations for books with user ownership
- **Reviews System**: Users can add, view, and delete reviews for books
- **Tags System**: Flexible tagging system for book categorization
- **Authentication**: JWT-based authentication with access and refresh tokens
- **Role-Based Access**: Admin and user roles with different permissions
- **Email Integration**: Automated email sending for verification and password reset
- **Background Tasks**: Asynchronous task processing with Celery and Redis
- **Database**: PostgreSQL with SQLModel ORM and Alembic migrations
- **Containerization**: Docker and Docker Compose ready

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLModel (SQLAlchemy)
- **Authentication**: JWT tokens with role-based access control
- **Background Tasks**: Celery with Redis broker
- **Email**: FastAPI-Mail with SMTP
- **Migrations**: Alembic
- **Containerization**: Docker & Docker Compose
- **Validation**: Pydantic models

## 📋 Requirements

- Python 3.11+
- PostgreSQL database
- Redis server
- SMTP email service (Gmail, etc.)

## 🔧 Installation & Setup

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bookly
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

### Option 2: Local Development

1. **Clone and setup virtual environment**
   ```bash
   git clone <repository-url>
   cd bookly
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Start Celery worker (separate terminal)**
   ```bash
   celery -A src.celery_tasks.c_app worker --loglevel=info
   ```

7. **Start Celery Flower (optional - monitoring)**
   ```bash
   celery -A src.celery_tasks.c_app flower --port=5555
   ```

## ⚙️ Environment Configuration

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_FROM=your-email@gmail.com
MAIL_FROM_NAME="Bookly Support"

# Application
DOMAIN=localhost:8000
```

## 📊 Database Schema

The application uses the following main models:

- **User**: User accounts with authentication and roles
- **Book**: Books with metadata and user ownership
- **Review**: User reviews for books with ratings
- **Tag**: Tags for categorizing books
- **BookTag**: Many-to-many relationship between books and tags

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/verify/{token}` - Email verification
- `GET /api/v1/auth/refresh_token` - Refresh access token
- `GET /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/password-reset-request` - Request password reset
- `POST /api/v1/auth/password-reset-confirm/{token}` - Confirm password reset

### Books
- `GET /api/v1/books/` - Get all books
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/{book_uid}` - Get book details
- `PATCH /api/v1/books/{book_uid}` - Update book
- `DELETE /api/v1/books/{book_uid}` - Delete book
- `GET /api/v1/books/user/{user_uid}` - Get user's books

### Reviews
- `GET /api/v1/reviews/` - Get all reviews (admin only)
- `POST /api/v1/reviews/book/{book_uid}` - Add review to book
- `GET /api/v1/reviews/{review_uid}` - Get specific review
- `DELETE /api/v1/reviews/{review_uid}` - Delete review

### Tags
- `GET /api/v1/tags/` - Get all tags
- `POST /api/v1/tags/` - Create new tag
- `PUT /api/v1/tags/{tag_uid}` - Update tag
- `DELETE /api/v1/tags/{tag_uid}` - Delete tag
- `POST /api/v1/tags/book/{book_uid}/tags` - Add tags to book

## 📖 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication & Authorization

The API uses JWT tokens for authentication:

1. **Register** a new account via `/auth/signup`
2. **Verify** your email using the link sent to your inbox
3. **Login** via `/auth/login` to get access and refresh tokens
4. **Include** the access token in the Authorization header: `Bearer <token>`

### User Roles
- **User**: Can manage their own books, add reviews, create tags
- **Admin**: Full access to all resources

## 🐳 Docker Services

When using Docker Compose, the following services are available:

- **app**: Main FastAPI application (port 8000)
- **redis**: Redis server for caching and task queue (port 6379)
- **celery-worker**: Background task processor
- **celery-flower**: Task monitoring dashboard (port 5555)

## 📧 Email Features

- **Account Verification**: Automatic email verification on signup
- **Password Reset**: Secure password reset via email
- **Background Processing**: All emails are sent asynchronously via Celery

## 🗄️ Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🧪 Development

### Project Structure
```
bookly/
├── src/
│   ├── auth/           # Authentication logic
│   ├── books/          # Book management
│   ├── reviews/        # Review system
│   ├── tags/           # Tag system
│   ├── db/            # Database configuration
│   ├── config.py      # Application configuration
│   ├── errors.py      # Error handling
│   └── middleware.py  # Custom middleware
├── migrations/        # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── main.py           # Application entry point
```

### Adding New Features

1. Create new modules in the `src/` directory
2. Define your models in `src/db/models.py`
3. Create Pydantic schemas for validation
4. Implement service layer logic
5. Add API routes
6. Create database migrations
7. Update tests

## 🚨 Common Issues

1. **Migration Errors**: Ensure database is running and accessible
2. **Redis Connection**: Check Redis service is running for background tasks
3. **Email Issues**: Verify SMTP credentials and app passwords for Gmail
4. **Token Errors**: Check JWT_SECRET configuration

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue on the GitHub repository.