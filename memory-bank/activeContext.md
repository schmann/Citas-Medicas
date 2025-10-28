# Active Context: Unidad Médica

## Current Work Focus

**Initialization Phase**: Establishing foundational infrastructure and documentation
- Memory Bank system initialization completed
- Project structure analysis and documentation in progress
- Base system components identified and documented

## Recent Changes & Current State

### Database Models Status
- ✅ **Core Patient Management**: `Paciente`, `DireccionPaciente` models fully implemented
- ✅ **Medical Professional Models**: `UsuarioMedico`, `MedicoEspecialidad` with registry integration
- ✅ **Appointment Scheduling**: `HorarioCita`, `CitasReservadas`, `Cita` models in place
- ✅ **Geographic Infrastructure**: Venezuelan administrative divisions (País→Estado→Ciudad→Municipio→Parroquia)
- ✅ **Facility Management**: `Consultorio` model for clinic room/office management
- ✅ **Financial Integration**: `Banco`, `DatosSeniat` models for payment processing

### Application Structure Status
- ✅ **Django Apps**: `citas` (core appointments), `web` (public interface) apps structured
- ✅ **Admin Interface**: Jazzmin configuration with hierarchical menu structure
- ✅ **URL Configuration**: Clean URL patterns separating public and admin routes
- ✅ **API Layer**: REST API foundations with DRF integration
- ✅ **Static Assets**: CSS, JavaScript, image management structure
- ✅ **Template System**: Bootstrap-based responsive templates

### External Integrations Status
- ✅ **Google Calendar**: API integration code present, OAuth2 configuration
- ✅ **Geographic Data**: Venezuelan administrative divisions loaded
- ✅ **Authentication**: Django built-in auth with extensible user model
- ⚠️ **SMS/Email Services**: Framework ready, configuration needed
- ❌ **Telemedicine Platform**: Integration interfaces defined, not implemented

## Active User Stories & Features

### 🔄 Currently Implementing
1. **Patient Self-Registration** (`web.views.patient_registration`)
   - Online form with validation
   - Geographic location selection with cascading dropdowns
   - Email verification and account activation

2. **Doctor Availability Management** (`citas.views.doctor_schedule`)
   - Recurring schedule creation
   - Specialty-based availability blocks
   - Google Calendar synchronization

3. **Appointment Booking System** (`citas.views.appointment_booking`)
   - Real-time availability checking
   - Patient-doctor-specialty matching
   - Conflict prevention and validation

### 📋 Next Priority Features
1. **Appointment Management Dashboard**
   - Doctor's daily schedule view
   - Patient history and upcoming appointments
   - Cancellations and rescheduling

2. **Patient Portal**
   - Appointment booking interface
   - Medical history access
   - Payment and billing information

3. **Administrative Reporting**
   - Clinic utilization reports
   - Doctor performance metrics
   - Revenue and patient statistics

## Important Patterns & Preferences

### Coding Standards
- **Model Naming**: Spanish field names for domain accuracy, English technical names
- **URL Patterns**: RESTful design with clear resource hierarchies
- **Template Organization**: Component-based structure with reusable includes
- **JavaScript Integration**: Progressive enhancement with jQuery for DOM manipulation

### Database Design Patterns
- **Mixed Management**: `managed=True` for new tables, `managed=False` for legacy data
- **Indexing Strategy**: Foreign key and frequently queried field indexes
- **Relationship Types**: Explicit many-to-many tables for specialty assignments

### UI/UX Patterns
- **Responsive Design**: Mobile-first approach with Bootstrap breakpoints
- **Form Validation**: Client-side validation with server-side confirmation
- **Navigation Hierarchy**: Jazzmin admin menu matching Venezuelan healthcare workflows

## Current Challenges & Blockers

### Technical Debt Issues
1. **Model Inconsistencies**: Some models use `managed=False` with hardcoded db_column references
2. **Mixed Application Logic**: Business logic spread between views and model methods
3. **Synchronous Operations**: Heavy API calls blocking user interactions

### Integration Challenges
1. **Google Calendar Sync**: Bidirectional synchronization reliability
2. **Geographic Data Accuracy**: Venezuelan administrative division updates
3. **Performance Optimization**: N+1 query issues in complex relationship traversals

### Process Improvements Needed
1. **Testing Strategy**: Currently minimal automated testing coverage
2. **Code Documentation**: Limited docstrings and inline comments
3. **Migration Management**: Database migration history needs cleanup

## Next Critical Actions

### Immediate (This Session)
1. **Complete Memory Bank**: Finish progress.md documentation
2. **Database Migration Check**: Verify all migrations run successfully
3. **Basic Functionality Test**: Confirm core CRUD operations working

### Short Term (Next Few Sessions)
1. **Patient Registration Flow**: Complete online registration system
2. **Doctor Availability Setup**: Implement schedule creation interface
3. **Appointment Booking**: Build the core booking workflow
4. **Basic Admin Reports**: Add essential reporting views

### Medium Term (Next Sprint)
1. **Google Calendar Integration**: Complete bidirectional sync
2. **Email/SMS Notifications**: Implement appointment reminders
3. **API Expansion**: Develop mobile app supporting endpoints
4. **Performance Optimization**: Address N+1 queries and caching

## Active Decisions Made

### Architecture Choices
- **Django Apps Structure**: Separate `citas` and `web` apps for clean separation
- **Database Strategy**: PostgreSQL with some legacy table integration
- **Admin Interface**: Jazzmin for modern administrative experience
- **API Framework**: DRF for REST API with future mobile app support

### Development Practices
- **Version Control**: Git with conventional commit messages
- **Environment Management**: `.env` files with `python-dotenv`
- **Code Quality**: Black for formatting, flake8 for linting
- **Documentation**: Memory Bank system for project continuity

### Deployment Strategy
- **Container Ready**: Docker configuration for easy deployment
- **Static Files**: Whitenoise for Django static file serving
- **Background Tasks**: Celery with Redis for async operations
- **Production Server**: Gunicorn WSGI server configuration
