# VulWeb - Code Vulnerability Detection ML Platform

A comprehensive web platform for code vulnerability detection using machine learning. This system provides an intuitive interface for managing models, datasets, and training tasks with real-time monitoring and visualization.

## Features

### 🤖 AI Chat Assistant (NEW!)
- Natural language interface for platform interaction
- Multi-agent system with specialized AI agents
- Real-time WebSocket communication
- Conversation history and context management
- Suggested queries and smart responses
- Mobile-responsive floating chat widget

### 🔧 Model Management
- Upload and register ML models
- View model information and performance metrics
- Support for multiple model types (vulnerability detection, fine-grained location)
- Version management

### 📊 Dataset Management
- Upload and store datasets
- Automatic format validation (JSON, CSV)
- Dataset statistics and preprocessing
- Support for code vulnerability detection data formats

### 🚀 Training & Validation
- Create and manage training tasks
- Real-time training progress monitoring
- Interactive metrics visualization with charts
- Training history and results analysis
- One-click training start

### 🎨 User Interface
- Modern, responsive web interface
- Intuitive navigation between modules
- Real-time data updates
- Interactive charts and visualizations
- AI-powered chat assistant

## Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLAlchemy with SQLite (can be switched to PostgreSQL)
- **Async Tasks**: Celery + Redis
- **API**: RESTful design with CORS support
- **WebSocket**: Flask-SocketIO for real-time chat
- **AI**: Multi-agent architecture for intelligent assistance

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: React Icons
- **WebSocket**: Socket.IO Client

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (for frontend)
- **WSGI Server**: Gunicorn (for backend)

## Project Structure

```
vulweb/
├── backend/
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── models.py
│   │   │   ├── datasets.py
│   │   │   └── training.py
│   │   ├── models/         # Database models
│   │   │   └── __init__.py
│   │   ├── services/       # Business logic
│   │   │   ├── dataset_service.py
│   │   │   └── training_service.py
│   │   └── utils/          # Utility functions
│   │       └── file_utils.py
│   ├── config/             # Configuration
│   │   └── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Models.js
│   │   │   ├── Datasets.js
│   │   │   └── Training.js
│   │   ├── services/       # API services
│   │   │   └── api.js
│   │   ├── styles/         # CSS styles
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   ├── nginx.conf
│   └── Dockerfile
└── docker-compose.yml
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)
- Redis (for async tasks)

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/Accessiry/vulweb.git
cd vulweb
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:5000

### Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python run.py
```

The backend will be available at http://localhost:5000

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

#### Redis Setup (for async tasks)

```bash
# Install Redis
# Ubuntu/Debian:
sudo apt-get install redis-server

# macOS:
brew install redis

# Start Redis
redis-server
```

## Usage Guide

### 0. Using AI Chat Assistant 🤖

**Access the Chat:**
- Click the chat button (💬) in the bottom-right corner of any page
- The chat widget will open with a welcome message

**Example Queries:**
- "Show all models"
- "List datasets with more than 100 samples"
- "Show running training tasks"
- "What file formats are supported?"
- "Show platform statistics"

**Features:**
- Natural language queries
- Suggested quick actions
- Conversation history
- Real-time responses
- Works across all pages

See [AI_CHAT_GUIDE.md](AI_CHAT_GUIDE.md) for detailed documentation.

### 1. Managing Models

**Add a New Model:**
1. Navigate to the "Models" page
2. Click "Add Model" button
3. Fill in model information:
   - Name (required)
   - Description
   - Version
   - Model Type
   - Upload model file (.pkl, .pt, .pth, .h5)
4. Click "Create Model"

**View Models:**
- All models are displayed in a grid layout
- Each card shows model name, description, type, version, and accuracy

**Delete Models:**
- Click the trash icon on any model card to delete it

### 2. Managing Datasets

**Upload a Dataset:**
1. Navigate to the "Datasets" page
2. Click "Add Dataset" button
3. Fill in dataset information:
   - Name (required)
   - Description
   - Upload dataset file (.json, .csv, .txt, .zip)
4. Click "Upload Dataset"

**View Dataset Statistics:**
- Each dataset card displays:
  - Format
  - File size
  - Number of samples
  - Number of vulnerable/safe samples
  - Preprocessing status

**Delete Datasets:**
- Click the trash icon on any dataset card to delete it

### 3. Training Models

**Start Training:**
1. Navigate to the "Training" page
2. Click "Start Training" button
3. Configure training task:
   - Task name
   - Select a model
   - Select a dataset
   - Number of epochs
4. Click "Start Training"

**Monitor Training:**
- View real-time training progress
- Interactive charts showing:
  - Loss over time
  - Accuracy over time
  - Training vs Validation metrics
- Current metrics displayed in cards:
  - Loss
  - Accuracy
  - Validation Loss
  - Validation Accuracy

**Manage Tasks:**
- Stop running tasks
- Delete completed tasks
- View training history

## API Documentation

### Models API

```
GET    /api/models          - Get all models
GET    /api/models/:id      - Get model by ID
POST   /api/models          - Create new model
PUT    /api/models/:id      - Update model
DELETE /api/models/:id      - Delete model
```

### Datasets API

```
GET    /api/datasets             - Get all datasets
GET    /api/datasets/:id         - Get dataset by ID
POST   /api/datasets             - Create new dataset
PUT    /api/datasets/:id         - Update dataset
DELETE /api/datasets/:id         - Delete dataset
GET    /api/datasets/:id/stats   - Get dataset statistics
```

### Training API

```
GET    /api/training/tasks                - Get all training tasks
GET    /api/training/tasks/:id            - Get task by ID
POST   /api/training/tasks                - Create new training task
POST   /api/training/tasks/:id/stop       - Stop running task
GET    /api/training/tasks/:id/metrics    - Get task metrics
POST   /api/training/tasks/:id/metrics    - Add task metric
DELETE /api/training/tasks/:id            - Delete task
```

### Chat API (NEW!)

```
POST   /api/chat/message    - Send chat message
GET    /api/chat/history    - Get conversation history
POST   /api/chat/clear      - Clear conversation history
```

**WebSocket Events:**
- `connect` - Connect to chat server
- `join` - Join a session
- `chat_message` - Send message
- `chat_response` - Receive response

See [AI_CHAT_GUIDE.md](AI_CHAT_GUIDE.md) for detailed API documentation.
POST   /api/training/tasks/:id/metrics    - Add task metric
DELETE /api/training/tasks/:id            - Delete task
```

## Integrating Your Training Code

The platform provides a standardized interface for integrating custom training code. 

### Training Service Integration

Edit `backend/app/services/training_service.py`:

```python
def start_training_task(task_id, config):
    """Integrate your training code here"""
    task = TrainingTask.query.get(task_id)
    
    # Import your training module
    from your_module import train_model
    
    # Call your training function
    train_model(
        model_path=task.model.file_path,
        dataset_path=task.dataset.file_path,
        epochs=config.get('epochs'),
        task_id=task_id
    )
```

### Reporting Training Progress

During training, report metrics to the API:

```python
import requests

def report_progress(task_id, epoch, metrics):
    requests.post(
        f'http://localhost:5000/api/training/tasks/{task_id}/metrics',
        json={
            'epoch': epoch,
            'loss': metrics['loss'],
            'accuracy': metrics['accuracy'],
            'validation_loss': metrics['val_loss'],
            'validation_accuracy': metrics['val_accuracy'],
            'learning_rate': metrics['lr']
        }
    )
```

## Configuration

### Backend Configuration

Edit `backend/config/config.py` or set environment variables:

```python
SECRET_KEY                # Application secret key
DATABASE_URL             # Database connection string
CELERY_BROKER_URL        # Redis URL for Celery
CELERY_RESULT_BACKEND    # Redis URL for results
UPLOAD_FOLDER            # Directory for uploads
MAX_CONTENT_LENGTH       # Max file size (bytes)
```

### Frontend Configuration

Create `.env` file in frontend directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Code Style

Backend uses Python best practices with Flask conventions.
Frontend follows React best practices with functional components and hooks.

## Architecture

### System Architecture

```
┌─────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   Backend   │
│   (React)   │  HTTP   │   (Flask)   │
└─────────────┘         └──────┬──────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
                ┌───▼───┐  ┌───▼───┐  ┌──▼───┐
                │SQLite │  │ Redis │  │Celery│
                └───────┘  └───────┘  └──────┘
```

### Design Patterns

- **Backend**: MVC pattern with blueprints
- **Frontend**: Component-based architecture
- **API**: RESTful design
- **Database**: Repository pattern with SQLAlchemy ORM

## Extensibility

### Adding New Model Types

The system is designed for extensibility with reserved interfaces for:
- Fine-grained vulnerability location
- Custom model architectures
- Additional preprocessing steps

### Adding New Dataset Formats

Extend `backend/app/services/dataset_service.py` to support new formats:

```python
def analyze_custom_format(file_path):
    # Your custom format analysis
    return {
        'num_samples': count,
        'num_vulnerable': vulnerable_count,
        'num_safe': safe_count
    }
```

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version (3.10+)
- Ensure all dependencies are installed
- Verify database is accessible

**Frontend won't start:**
- Check Node version (18+)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall

**Training tasks not starting:**
- Ensure Redis is running
- Check Celery worker status
- Verify dataset and model files exist

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@vulweb.com

## Roadmap

- [ ] PostgreSQL support
- [ ] User authentication and authorization
- [ ] Advanced model performance analytics
- [ ] Distributed training support
- [ ] Model versioning and comparison
- [ ] API rate limiting
- [ ] Kubernetes deployment support
- [ ] Fine-grained vulnerability location module
- [ ] Model ensemble support
- [ ] Advanced data augmentation

## Acknowledgments

Built with modern web technologies for the code vulnerability detection research community.