# Contributing to VulWeb

Thank you for your interest in contributing to VulWeb! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Setting Up Development Environment

1. Fork the repository on GitHub

2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/vulweb.git
cd vulweb
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/Accessiry/vulweb.git
```

4. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

5. Set up frontend:
```bash
cd frontend
npm install
```

6. Run tests to verify setup:
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests (when available)
cd frontend
npm test
```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Test your changes thoroughly
3. Commit with descriptive messages

```bash
git add .
git commit -m "Add feature: description of what you added"
```

### Keeping Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

## Code Style

### Python (Backend)

Follow PEP 8 style guide:

```python
# Good
def create_model(name, description):
    """Create a new model with given parameters"""
    model = Model(name=name, description=description)
    return model

# Use type hints
def get_dataset(dataset_id: int) -> Dataset:
    """Get dataset by ID"""
    return Dataset.query.get(dataset_id)
```

Key points:
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)
- Use docstrings for functions and classes
- Type hints for function parameters and returns

### JavaScript/React (Frontend)

Follow React best practices:

```javascript
// Use functional components with hooks
function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(initialValue);
  
  useEffect(() => {
    // Effect logic
  }, [dependencies]);
  
  return (
    <div className="my-component">
      {/* JSX content */}
    </div>
  );
}

// Use meaningful variable names
const handleSubmit = async (event) => {
  event.preventDefault();
  // Handle logic
};
```

Key points:
- Use functional components with hooks
- 2 spaces for indentation
- Use meaningful component and variable names
- Keep components small and focused

### CSS

```css
/* Use BEM-like naming */
.component-name {
  property: value;
}

.component-name__element {
  property: value;
}

.component-name--modifier {
  property: value;
}
```

## Testing

### Backend Testing

Write tests for all new features:

```python
# tests/test_feature.py
import pytest

class TestNewFeature:
    def test_feature_works(self, client):
        """Test that the feature works as expected"""
        response = client.get('/api/endpoint')
        assert response.status_code == 200
        assert 'expected_key' in response.json
    
    def test_feature_handles_errors(self, client):
        """Test error handling"""
        response = client.post('/api/endpoint', data={})
        assert response.status_code == 400
```

Run tests:
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Testing

Write tests for components:

```javascript
// ComponentName.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import ComponentName from './ComponentName';

test('renders component correctly', () => {
  render(<ComponentName />);
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
});

test('handles user interaction', () => {
  render(<ComponentName />);
  const button = screen.getByRole('button');
  fireEvent.click(button);
  // Assert expected behavior
});
```

## Project Structure

Understanding the project structure:

```
vulweb/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints (add new routes here)
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   ├── config/               # Configuration
│   └── tests/                # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   └── styles/           # CSS styles
│   └── public/               # Static files
└── docs/                     # Documentation
```

## Types of Contributions

### Bug Fixes

1. Check if the bug is already reported in Issues
2. If not, create a new issue describing:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
3. Reference the issue in your pull request

### New Features

1. Discuss the feature in Issues first
2. Wait for maintainer approval
3. Implement the feature
4. Add tests
5. Update documentation
6. Submit pull request

### Documentation

Documentation improvements are always welcome:
- Fix typos
- Improve clarity
- Add examples
- Translate documentation

## Submitting Changes

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add yourself to CONTRIBUTORS.md
4. Create pull request with description:
   - What changes you made
   - Why you made them
   - Any relevant issue numbers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Development Tips

### Backend Development

1. **Database Migrations**
```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

2. **Debug Mode**
```bash
export FLASK_ENV=development
python run.py
```

3. **API Testing**
```bash
# Use curl or httpie
curl -X GET http://localhost:5000/api/models
```

### Frontend Development

1. **Hot Reload**
```bash
npm start  # Changes auto-reload
```

2. **Component Development**
- Create reusable components
- Use PropTypes or TypeScript for type checking
- Keep state management simple

3. **API Integration**
```javascript
// Use the API service
import { modelsAPI } from '../services/api';

const fetchData = async () => {
  const response = await modelsAPI.getAll();
  setData(response.data);
};
```

## Common Tasks

### Adding a New API Endpoint

1. Define the route in `backend/app/api/`:
```python
@blueprint.route('/new-endpoint', methods=['GET'])
def new_endpoint():
    # Implementation
    return jsonify(data), 200
```

2. Register the blueprint in `backend/app/__init__.py`

3. Add tests in `backend/tests/`

4. Update API documentation in README.md

### Adding a New React Component

1. Create component file in `frontend/src/components/`
2. Create corresponding CSS file in `frontend/src/styles/`
3. Import and use in parent component or route
4. Add tests if needed

### Adding a New Database Model

1. Define model in `backend/app/models/__init__.py`
2. Create migration:
```bash
flask db migrate -m "Add new model"
flask db upgrade
```
3. Add API endpoints
4. Add tests

## Questions?

If you have questions:
1. Check existing documentation
2. Search through Issues
3. Create a new issue with your question

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing to VulWeb!
