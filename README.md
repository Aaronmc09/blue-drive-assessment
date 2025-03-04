# Django Docker Project

This is a Django application containerized with Docker, using PostgreSQL as the database.

## Prerequisites

- Docker
- Docker Compose
- Git

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create environment file:
```bash
cp .env.sample .env
```

3. Update the `.env` file with your desired configuration:
- Set a secure `SECRET_KEY`
- Update `DB_PASSWORD` and `DJANGO_ADMIN_PASSWORD` with strong passwords
- Modify other variables as needed

## Running the Application

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Once the containers are running, you can access:
- Django application: http://localhost:8000
- PostgreSQL database: localhost:5432

## Project Structure

- `Dockerfile`: Contains the configuration for building the Django application container
- `docker-compose.yml`: Defines and configures the application services (web and database)
- `requirements.txt`: Lists all Python dependencies
- `entrypoint.sh`: Script that runs when the container starts

## Database

The project uses PostgreSQL 13 with the following default configuration:
- Database name: specified in DB_NAME
- User: specified in DB_USER
- Password: specified in DB_PASSWORD
- Host: db
- Port: 5432

## Development

The application code is mounted as a volume, so any changes you make to the local files will be reflected in the container.

To run management commands:
```bash
docker-compose exec web python manage.py <command>
```

Common commands:
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create a superuser
docker-compose exec web python manage.py createsuperuser
```

## Stopping the Application

To stop the application:
```bash
docker-compose down
```

To stop the application and remove volumes:
```bash
docker-compose down -v
```

## Authentication Screens

### Login
The login screen is accessible at `/login/` and requires:
- Username/Email
- Password

Default admin login:
- Email: specified in DJANGO_ADMIN_EMAIL (default: admin@django.com)
- Password: specified in DJANGO_ADMIN_PASSWORD

### Registration
New users can register at `/register/` by providing:
- Email address
- Username
- Password
- Password confirmation

After registration, users will need to:
1. Verify their email address (if email verification is enabled)
2. Log in using their credentials

### Password Reset
Users can reset their password at `/password-reset/` by:
1. Entering their email address
2. Following the reset link sent to their email
3. Setting a new password 