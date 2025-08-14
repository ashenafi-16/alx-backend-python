# Docker Compose Setup for Messaging App

## Overview
This project now uses Docker Compose to manage multiple services:
- **Web Service**: Django messaging application
- **Database Service**: MySQL 8.0 database

## Files Created/Modified

### 1. docker-compose.yml
- Defines two services: `web` (Django) and `db` (MySQL)
- Sets up networking between services
- Configures volume for persistent MySQL data
- Includes health checks for database service

### 2. .env
- Contains environment variables for database configuration
- **IMPORTANT**: This file is in .gitignore and should never be committed to version control
- Contains sensitive information like database passwords

### 3. requirements.txt
- Added `mysqlclient==2.2.0` for MySQL database connectivity

### 4. Dockerfile
- Added MySQL client development libraries
- Installs `default-libmysqlclient-dev` and `pkg-config`

### 5. messaging_app/settings.py
- Updated database configuration to use MySQL instead of SQLite
- Reads database settings from environment variables
- Connects to MySQL service named `db` (Docker Compose service name)

### 6. .gitignore
- Excludes .env file and other sensitive files
- Prevents accidental commit of environment variables

## How to Use

### 1. Start the Services
```bash
docker-compose up --build -d
```

### 2. Check Service Status
```bash
docker-compose ps
```

### 3. View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db
```

### 4. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Stop Services
```bash
docker-compose down
```

### 6. Rebuild After Changes
```bash
docker-compose up --build -d
```

## Service Details

### Web Service (Django)
- **Port**: 8000 (accessible at http://localhost:8000)
- **Database Host**: `db` (internal Docker network)
- **Volume Mount**: Current directory mounted for development
- **Command**: Runs migrations and starts Django development server

### Database Service (MySQL)
- **Port**: 3307 (accessible at localhost:3307)
- **Internal Port**: 3306 (within Docker network)
- **Database**: messaging_db
- **User**: messaging_user
- **Password**: messaging_password123
- **Root Password**: root_password123
- **Volume**: mysql_data (persistent storage)

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| MYSQL_DATABASE | messaging_db | Database name |
| MYSQL_USER | messaging_user | Database user |
| MYSQL_PASSWORD | messaging_password123 | Database password |
| MYSQL_ROOT_PASSWORD | root_password123 | Root password |
| DJANGO_ALLOWED_HOSTS | * | Django allowed hosts |
| DJANGO_DEBUG | True | Django debug mode |

## Network Architecture

```
Host Machine (Windows)
├── Port 8000 → Web Service (Django)
├── Port 3307 → Database Service (MySQL)
└── Docker Network: messaging_app_messaging_network
    ├── web service (internal)
    └── db service (internal)
```

## Database Connection

Django connects to MySQL using:
- **Host**: `db` (Docker Compose service name)
- **Port**: 3306 (internal MySQL port)
- **Database**: messaging_db
- **User**: messaging_user
- **Password**: messaging_password123

## Security Notes

1. **Environment Variables**: Never commit .env file to version control
2. **Database Passwords**: Use strong passwords in production
3. **Port Exposure**: Only necessary ports are exposed to host
4. **Network Isolation**: Services communicate through Docker network

## Troubleshooting

### Port Conflicts
If port 3306 is already in use:
- Change the host port in docker-compose.yml: `"3308:3306"`
- Or stop existing MySQL service

### Database Connection Issues
- Check if MySQL service is healthy: `docker-compose ps`
- View database logs: `docker-compose logs db`
- Ensure environment variables are set correctly

### Django Migration Issues
- Check web service logs: `docker-compose logs web`
- Ensure database service is running before web service

## Production Considerations

1. **Use Production WSGI Server**: Replace `runserver` with `gunicorn` or `uwsgi`
2. **Environment Variables**: Use proper production values
3. **Database Security**: Use strong passwords and limit network access
4. **SSL/TLS**: Enable HTTPS for production deployments
5. **Monitoring**: Add health checks and logging
6. **Backup**: Implement database backup strategies

## API Endpoints

After setup, your API endpoints are available at:
- **Admin**: http://localhost:8000/admin/
- **API Base**: http://localhost:8000/api/
- **Conversations**: http://localhost:8000/api/conversations/
- **Messages**: http://localhost:8000/api/conversations/{id}/messages/
- **DRF Login**: http://localhost:8000/api-auth/login/

## Next Steps

1. **Test the API**: Create users and conversations
2. **Add Authentication**: Implement JWT or session-based auth
3. **Add More Services**: Redis for caching, Celery for background tasks
4. **Production Deployment**: Use proper production settings
5. **Monitoring**: Add logging and health monitoring
