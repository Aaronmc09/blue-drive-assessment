# Django Docker Project

This is a Django application containerized with Docker, using PostgreSQL as the database.

## Prerequisites

- Docker
- Docker Compose
- Git

## Project Setup

1. Clone the repository:
```bash
git clone git@github.com:Aaronmc09/blue-drive-assessment.git
cd blue-drive-assessment
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

## Authentication Screens

### Login
The login screen is accessible at `/auth/login/` and requires:
- Email (used as the primary identifier)
- Password

Default admin login:
- Email: specified in DJANGO_ADMIN_EMAIL (default: admin@django.com)
- Password: specified in DJANGO_ADMIN_PASSWORD

## Adding New Users

There are two ways to create new users in the system:

### 1. Via Django Admin Interface
1. Log in to the admin interface at `/admin/` using admin credentials
2. Navigate to "Users" under "Authentication and Authorization"
3. Click "Add User" button
4. Fill in the required fields:
   - Email (required)
   - Password
   - Password confirmation
5. Click "Save"
6. Optionally, set additional fields like:
   - Username (optional)
   - First name
   - Last name
   - Staff status
   - Superuser status

### 2. Via Command Line
Create a new user using the management command:
```bash
# For regular user
docker-compose exec web python manage.py createsuperuser --email=user@example.com

# For superuser (admin access)
docker-compose exec web python manage.py createsuperuser
```

Note: The system uses email addresses as the primary identifier for users. Username is optional. 

## Using the application

1. First, you must login at `/auth/login/`
2. Access the List and Create APIs at `/api/v1/posts/`
3. Access Details, Update, Delete at `/api/v1/posts/<post_id>/`
4. Access Add Comment action API at `/api/v1/posts/<post_id>/add_comment/`

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

# Run unit tests
docker-compose exec web python manage.py test
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
