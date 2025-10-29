# Project Structure

This document provides an overview of the VulWeb platform project structure.

## Directory Tree

```
vulweb/
├── backend/                          # Backend application (Flask)
│   ├── app/                          # Main application package
│   │   ├── __init__.py              # Application factory
│   │   ├── api/                     # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── models.py           # Model management API
│   │   │   ├── datasets.py         # Dataset management API
│   │   │   └── training.py         # Training task API
│   │   ├── models/                  # Database models
│   │   │   └── __init__.py         # Model, Dataset, TrainingTask, TrainingMetric
│   │   ├── services/                # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── dataset_service.py  # Dataset analysis
│   │   │   └── training_service.py # Training management
│   │   └── utils/                   # Utility functions
│   │       ├── __init__.py
│   │       └── file_utils.py       # File handling utilities
│   ├── config/                      # Configuration
│   │   ├── __init__.py
│   │   └── config.py               # Environment configs
│   ├── tests/                       # Unit tests
│   │   ├── __init__.py
│   │   └── test_api.py             # API tests
│   ├── Dockerfile                   # Docker configuration
│   ├── requirements.txt             # Python dependencies
│   ├── run.py                       # Application entry point
│   ├── training_example.py          # Training integration example
│   ├── .env.example                 # Environment variables template
│   ├── uploads/                     # Uploaded files (gitignored)
│   │   ├── models/                 # Model files
│   │   └── datasets/               # Dataset files
│   └── training_outputs/            # Training results (gitignored)
│
├── frontend/                         # Frontend application (React)
│   ├── src/                         # Source code
│   │   ├── components/              # React components
│   │   │   ├── Models.js           # Model management UI
│   │   │   ├── Datasets.js         # Dataset management UI
│   │   │   └── Training.js         # Training monitoring UI
│   │   ├── services/                # API services
│   │   │   └── api.js              # API client
│   │   ├── styles/                  # CSS styles
│   │   │   ├── Models.css
│   │   │   ├── Datasets.css
│   │   │   └── Training.css
│   │   ├── App.js                   # Main App component
│   │   ├── App.css                  # App styles
│   │   ├── index.js                 # Entry point
│   │   └── index.css                # Global styles
│   ├── public/                      # Static files
│   │   └── index.html              # HTML template
│   ├── Dockerfile                   # Docker configuration
│   ├── nginx.conf                   # Nginx configuration
│   └── package.json                 # Node dependencies
│
├── docker-compose.yml               # Docker Compose configuration
├── .gitignore                       # Git ignore rules
├── README.md                        # Main documentation
├── QUICKSTART.md                    # Quick start guide
├── DEPLOYMENT.md                    # Deployment guide
└── CONTRIBUTING.md                  # Contribution guidelines
```

## Backend Components

### API Layer (`backend/app/api/`)

**models.py** - Model Management API
- `GET /api/models` - List all models
- `GET /api/models/:id` - Get model details
- `POST /api/models` - Create new model
- `PUT /api/models/:id` - Update model
- `DELETE /api/models/:id` - Delete model

**datasets.py** - Dataset Management API
- `GET /api/datasets` - List all datasets
- `GET /api/datasets/:id` - Get dataset details
- `POST /api/datasets` - Upload new dataset
- `PUT /api/datasets/:id` - Update dataset
- `DELETE /api/datasets/:id` - Delete dataset
- `GET /api/datasets/:id/stats` - Get dataset statistics

**training.py** - Training Task API
- `GET /api/training/tasks` - List all training tasks
- `GET /api/training/tasks/:id` - Get task details
- `POST /api/training/tasks` - Create new training task
- `POST /api/training/tasks/:id/stop` - Stop running task
- `GET /api/training/tasks/:id/metrics` - Get task metrics
- `POST /api/training/tasks/:id/metrics` - Add metric (internal)
- `DELETE /api/training/tasks/:id` - Delete task

### Database Models (`backend/app/models/`)

**Model** - ML model information
- id, name, description, version
- model_type, file_path
- accuracy, precision, recall, f1_score
- created_at, updated_at

**Dataset** - Dataset information
- id, name, description, file_path
- format, size, num_samples
- num_vulnerable, num_safe
- preprocessing_status
- created_at, updated_at

**TrainingTask** - Training task information
- id, name, model_id, dataset_id
- status, progress, current_epoch, total_epochs
- loss, accuracy, validation_loss, validation_accuracy
- start_time, end_time, error_message
- created_at, updated_at

**TrainingMetric** - Training metrics per epoch
- id, task_id, epoch
- loss, accuracy, validation_loss, validation_accuracy
- learning_rate, timestamp

### Services (`backend/app/services/`)

**dataset_service.py** - Dataset Analysis
- `analyze_dataset()` - Analyze dataset and extract statistics
- `analyze_json_dataset()` - JSON format handler
- `analyze_csv_dataset()` - CSV format handler

**training_service.py** - Training Management
- `start_training_task()` - Start training process
- `simulate_training()` - Demo training simulation

### Configuration (`backend/config/`)

**config.py** - Application Configuration
- `Config` - Base configuration
- `DevelopmentConfig` - Development settings
- `ProductionConfig` - Production settings
- `TestingConfig` - Testing settings

## Frontend Components

### Pages/Components (`frontend/src/components/`)

**Models.js** - Model Management
- List all models in grid layout
- Create new model form
- Delete model functionality
- Model information display

**Datasets.js** - Dataset Management
- List all datasets in grid layout
- Upload new dataset form
- Dataset statistics display
- Delete dataset functionality

**Training.js** - Training & Monitoring
- Training task list
- Create training task form
- Real-time metrics visualization
- Interactive charts (loss, accuracy)
- Start/stop task controls

### Services (`frontend/src/services/`)

**api.js** - API Client
- `modelsAPI` - Model API calls
- `datasetsAPI` - Dataset API calls
- `trainingAPI` - Training API calls
- Axios configuration with base URL

### Styles (`frontend/src/styles/`)

**Models.css** - Model component styling
**Datasets.css** - Dataset component styling
**Training.css** - Training component styling

## Configuration Files

### Docker

**Dockerfile** (backend) - Backend container configuration
- Python 3.10 base image
- Dependencies installation
- Gunicorn WSGI server

**Dockerfile** (frontend) - Frontend container configuration
- Node.js build stage
- Nginx production stage
- Static file serving

**docker-compose.yml** - Multi-container orchestration
- Backend service (Flask)
- Frontend service (React + Nginx)
- Redis service (Celery broker)
- Celery worker service
- Volume mappings
- Network configuration

**nginx.conf** - Nginx configuration
- Static file serving
- API proxy to backend
- SPA routing support

## File Organization Principles

### Backend

1. **Separation of Concerns**
   - API layer handles HTTP requests/responses
   - Services contain business logic
   - Models define data structure
   - Utils provide reusable functions

2. **Module Structure**
   - Each module has its own directory
   - `__init__.py` makes it a package
   - Related functionality grouped together

3. **Configuration**
   - Environment-based configuration
   - Sensitive data in environment variables
   - Defaults provided for development

### Frontend

1. **Component-Based**
   - Each feature is a component
   - Components are self-contained
   - Styles are co-located

2. **Service Layer**
   - API calls abstracted into services
   - Consistent error handling
   - Reusable across components

3. **Styling**
   - Component-specific styles
   - Global styles in App.css
   - Responsive design patterns

## Key File Descriptions

### Backend Files

- **app/__init__.py** - Application factory pattern, creates and configures Flask app
- **run.py** - Entry point, starts development server
- **config/config.py** - Environment-based configuration management
- **requirements.txt** - Python package dependencies
- **.env.example** - Template for environment variables

### Frontend Files

- **src/index.js** - React application entry point
- **src/App.js** - Main application component with routing
- **package.json** - Node.js dependencies and scripts
- **public/index.html** - HTML template

### Documentation Files

- **README.md** - Comprehensive platform documentation
- **QUICKSTART.md** - Quick start guide
- **DEPLOYMENT.md** - Production deployment guide
- **CONTRIBUTING.md** - Contribution guidelines
- **PROJECT_STRUCTURE.md** - This file

## File Naming Conventions

### Backend
- Python files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_CASE`

### Frontend
- JavaScript files: `PascalCase.js` (components)
- CSS files: `PascalCase.css`
- Variables/functions: `camelCase`
- Constants: `UPPER_CASE`

## Extension Points

### Adding New Features

**Backend:**
1. Create new API endpoint in `app/api/`
2. Add business logic in `app/services/`
3. Update models in `app/models/` if needed
4. Add tests in `tests/`

**Frontend:**
1. Create component in `src/components/`
2. Add styles in `src/styles/`
3. Update API service in `src/services/api.js`
4. Add route in `src/App.js` if needed

### Customization

**Training Integration:**
- Edit `backend/app/services/training_service.py`
- See `backend/training_example.py` for examples

**Dataset Formats:**
- Extend `backend/app/services/dataset_service.py`
- Add new format analyzers

**UI Customization:**
- Modify component CSS in `frontend/src/styles/`
- Update components in `frontend/src/components/`

## Build Outputs

### Backend
- `app.db` - SQLite database (gitignored)
- `uploads/` - User uploaded files (gitignored)
- `training_outputs/` - Training results (gitignored)

### Frontend
- `build/` - Production build (gitignored)
- `node_modules/` - Dependencies (gitignored)

## Dependencies

### Backend Key Dependencies
- Flask 3.0.0 - Web framework
- SQLAlchemy 2.0.23 - Database ORM
- Flask-CORS 4.0.0 - CORS support
- Celery 5.3.4 - Async tasks
- Redis 5.0.1 - Task broker
- Gunicorn 21.2.0 - WSGI server
- pytest 7.4.3 - Testing framework

### Frontend Key Dependencies
- React 18.2.0 - UI framework
- React Router 6.20.0 - Routing
- Axios 1.6.2 - HTTP client
- Recharts 2.10.3 - Charts
- React Icons 4.12.0 - Icons
- React Scripts 5.0.1 - Build tools

## Development vs Production

### Development
- SQLite database
- Debug mode enabled
- Hot reload for both backend and frontend
- Detailed error messages

### Production
- PostgreSQL recommended
- Debug mode disabled
- Static files served by Nginx
- Error logging to files
- Gunicorn with multiple workers

## Security Considerations

### File Locations
- Sensitive files in .gitignore
- Uploads stored outside web root
- Environment variables for secrets
- Database credentials not in code

### Access Control
- CORS configured properly
- File upload size limits
- File type validation
- Input sanitization

This structure is designed for scalability, maintainability, and ease of development.
