# Technology Context: Unidad Médica

## Core Technologies

### Backend Framework
- **Django 5.2.7**: Primary web framework providing ORM, authentication, admin interface
- **Python 3.14**: Runtime environment with modern async capabilities
- **Django REST Framework**: API-first design with JSON serialization

### Database & Storage
- **PostgreSQL 15+**: Primary database with JSON fields and geospatial support
- **Redis 5.0.1**: Session caching and background task queuing
- **Pillow 12.0.0**: Image processing for doctor photos and documents

### Frontend Technologies
- **HTML5/CSS3**: Semantic markup with responsive design
- **JavaScript (ES6+)**: Client-side interactivity and validation
- **Bootstrap**: UI framework for consistent styling
- **jQuery**: DOM manipulation and AJAX requests

### External Integrations
- **Google Calendar API**: Bidirectional calendar synchronization
- **Google OAuth2**: Secure authentication flows
- **Venezuelan DNI systems**: ID validation and demographic data
- **Twilio/SMS Services**: Appointment reminders (future)

## Development Environment

### Local Development Setup
```bash
# Virtual environment activation
python -m venv venvum
venvum\Scripts\activate  # Windows
source venvum/bin/activate  # Linux/Mac

# Dependencies installation
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Superuser creation
python manage.py createsuperuser

# Development server
python manage.py runserver
```

### Environment Variables (`.env`)
```env
# Django Configuration
DEBUG=True
SECRET_KEY=django-insecure-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=unidad_medica
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Google API (OAuth2)
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-secret
GOOGLE_OAUTH2_REDIRECT_URI=http://localhost:8000/oauth2callback

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=admin@unidadmedica.com
EMAIL_HOST_PASSWORD=password

# Redis/Celery (Background Tasks)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Key Dependencies & Versions

### Web Framework
```
Django==5.2.7
django-jazzmin==3.0.1        # Modern admin interface
django-cors-headers==4.3.1    # CORS configuration
django-axes==6.0.0           # Login attempt tracking
whitenoise==6.7.0            # Static file serving
```

### Database & APIs
```
psycopg2-binary==2.9.11       # PostgreSQL driver
google-api-python-client==2.185.0  # Google API integration
google-auth-oauthlib==1.2.1   # OAuth2 authentication
oauth2client==4.1.3           # Legacy OAuth support
```

### Async Processing
```
celery==5.3.6                 # Background task processing
redis==5.0.1                  # Caching and message broker
```

### Development Tools
```
pytest==8.2.0                 # Testing framework
pytest-django==4.8.0          # Django testing integration
pytest-cov==4.1.0             # Code coverage reporting
black==24.4.2                 # Code formatting
flake8==7.1.1                 # Linting
isort==5.13.2                 # Import sorting
```

### Production Deployment
```
gunicorn==22.0.0              # WSGI server
uvicorn==0.29.0               # ASGI server (future)
python-dotenv==1.0.1          # Environment variable management
requests==2.32.3              # HTTP client library
```

## Technical Constraints

### Database Limitations
- **Managed Tables**: Geographic data (paises, estados, ciudades, municipios, parroquias) uses existing database structure
- **Legacy Integration**: Some models reference unmanaged database tables
- **Performance**: Database queries optimized for Venezuelan geographic hierarchies

### API Limitations
- **Google Calendar Quotas**: 1 billion requests/day, but practical limits per user
- **Rate Limiting**: API calls constrained by Google and Venezuelan government services
- **Data Synchronization**: Bidirectional sync requires conflict resolution

### Browser Compatibility
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile Support**: iOS Safari, Android Chrome with responsive breakpoints
- **JavaScript Requirements**: ES6+ required for interactive features

## Development Patterns

### Code Organization
- **App Structure**: Modular Django apps (citas, web) with clear separation
- **Model Inheritance**: Abstract base classes for common functionality
- **View Patterns**: Class-based views with mixins for common behaviors
- **Template Structure**: Bootstrap-based components with custom CSS

### Testing Strategy
- **Unit Tests**: Individual component testing with pytest fixtures
- **Integration Tests**: API endpoint testing with DRF test client
- **End-to-End Tests**: Selenium for critical user journeys
- **Performance Tests**: Load testing for appointment booking workflows

### Deployment Architecture

#### Development Environment
```
┌─────────────────┐    ┌─────────────────┐
│   Browser       │◄──►│   Django Dev    │
│                 │    │   Server        │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   (Local)       │
                       └─────────────────┘
```

#### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │◄──►│   Django App    │◄──►│   PostgreSQL    │
│   (nginx)       │    │   (gunicorn)    │    │   (RDS/Aurora)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Redis Cache   │    │   Redis Queue   │
                       │                 │    │   (Celery)      │
                       └─────────────────┘    └─────────────────┘
```

### Monitoring & Logging
- **Django Logging**: Structured logging with context
- **Health Checks**: Database connectivity and API status endpoints
- **Performance Monitoring**: Query timing and memory usage tracking
- **Error Tracking**: Sentry integration for production error alerting

## Migration Path

### Current Technical Debt
- **Legacy Models**: Some Django models use `managed=False` for existing database tables
- **Mixed App Structure**: Business logic spread across multiple Django apps
- **Synchronous Processing**: Heavy operations blocking request-response cycle

### Planned Modernization
- **Async Views**: Django 5.2 async views for I/O bound operations
- **API First**: Complete migration to REST API with SPA frontend
- **Microservices**: Separate concerns into dedicated services
- **Containerization**: Full Docker/Kubernetes deployment pipeline
