# Quick Start Guide

This guide will help you get the VulWeb platform up and running quickly.

## Option 1: Quick Start with Docker (Recommended)

This is the fastest way to get started.

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

1. Clone the repository:
```bash
git clone https://github.com/Accessiry/vulweb.git
cd vulweb
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the platform:
- Frontend: http://localhost
- Backend API: http://localhost:5000

4. Stop the services:
```bash
docker-compose down
```

## Option 2: Development Setup

For development or customization, follow these steps.

### Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend:
```bash
python run.py
```

Backend will be available at http://localhost:5000

### Frontend Setup (in a new terminal)

1. Navigate to frontend:
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

Frontend will be available at http://localhost:3000

### Testing the Platform

Once both backend and frontend are running:

1. **Create a Model**
   - Open http://localhost:3000
   - Click "Models" in navigation
   - Click "Add Model"
   - Fill in the form and submit

2. **Upload a Dataset**
   - Click "Datasets" in navigation
   - Click "Add Dataset"
   - Upload a JSON or CSV file with vulnerability data
   - View statistics after processing

3. **Start Training**
   - Click "Training" in navigation
   - Click "Start Training"
   - Select a model and dataset
   - Set number of epochs
   - Monitor progress in real-time

## Sample Data

### Sample Dataset Format (JSON)

Create a file `sample_dataset.json`:

```json
[
  {
    "code": "def unsafe_query(user_input): return 'SELECT * FROM users WHERE id = ' + user_input",
    "label": 1,
    "vulnerability_type": "SQL Injection"
  },
  {
    "code": "def safe_query(user_input): cursor.execute('SELECT * FROM users WHERE id = ?', (user_input,))",
    "label": 0,
    "vulnerability_type": "None"
  },
  {
    "code": "eval(user_input)",
    "label": 1,
    "vulnerability_type": "Code Injection"
  }
]
```

### Sample Dataset Format (CSV)

Create a file `sample_dataset.csv`:

```csv
code,label,vulnerability_type
"def unsafe_query(user_input): return 'SELECT * FROM users WHERE id = ' + user_input",1,SQL Injection
"def safe_query(user_input): cursor.execute('SELECT * FROM users WHERE id = ?', (user_input,))",0,None
"eval(user_input)",1,Code Injection
```

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process or change the port in run.py
```

**Database errors:**
```bash
# Delete existing database and restart
rm backend/app.db
python backend/run.py
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Kill process or set different port
PORT=3001 npm start
```

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check REACT_APP_API_URL in frontend/.env

### Docker Issues

**Containers won't start:**
```bash
# View logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Customize the training service in `backend/app/services/training_service.py`
3. Integrate your own ML models
4. Extend dataset formats in `backend/app/services/dataset_service.py`

## Support

For issues or questions:
- Create an issue on GitHub
- Check the main README.md for more details
