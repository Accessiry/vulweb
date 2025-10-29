"""
Sample tests for the VulWeb platform

Run with: pytest tests/
"""

import pytest
import json
import os
import tempfile
from app import create_app
from app.models import db, Model, Dataset, TrainingTask


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestModelAPI:
    """Test Model API endpoints"""
    
    def test_get_models_empty(self, client):
        """Test getting models when none exist"""
        response = client.get('/api/models')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_model(self, client):
        """Test creating a model"""
        data = {
            'name': 'Test Model',
            'description': 'A test model',
            'version': '1.0',
            'model_type': 'vulnerability_detection'
        }
        response = client.post('/api/models', data=data)
        assert response.status_code == 201
        assert response.json['name'] == 'Test Model'
        assert response.json['id'] is not None
    
    def test_get_model(self, client):
        """Test getting a specific model"""
        # Create a model first
        data = {'name': 'Test Model', 'model_type': 'vulnerability_detection'}
        create_response = client.post('/api/models', data=data)
        model_id = create_response.json['id']
        
        # Get the model
        response = client.get(f'/api/models/{model_id}')
        assert response.status_code == 200
        assert response.json['name'] == 'Test Model'
    
    def test_update_model(self, client):
        """Test updating a model"""
        # Create a model
        data = {'name': 'Test Model', 'model_type': 'vulnerability_detection'}
        create_response = client.post('/api/models', data=data)
        model_id = create_response.json['id']
        
        # Update the model
        update_data = {'description': 'Updated description'}
        response = client.put(
            f'/api/models/{model_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['description'] == 'Updated description'
    
    def test_delete_model(self, client):
        """Test deleting a model"""
        # Create a model
        data = {'name': 'Test Model', 'model_type': 'vulnerability_detection'}
        create_response = client.post('/api/models', data=data)
        model_id = create_response.json['id']
        
        # Delete the model
        response = client.delete(f'/api/models/{model_id}')
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(f'/api/models/{model_id}')
        assert get_response.status_code == 404
    
    def test_create_duplicate_model(self, client):
        """Test creating a model with duplicate name"""
        data = {'name': 'Test Model', 'model_type': 'vulnerability_detection'}
        client.post('/api/models', data=data)
        
        # Try to create another with same name
        response = client.post('/api/models', data=data)
        assert response.status_code == 400


class TestDatasetAPI:
    """Test Dataset API endpoints"""
    
    def test_get_datasets_empty(self, client):
        """Test getting datasets when none exist"""
        response = client.get('/api/datasets')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_dataset(self, client):
        """Test creating a dataset"""
        # Create a temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                {'code': 'test', 'label': 1},
                {'code': 'test2', 'label': 0}
            ], f)
            temp_file = f.name
        
        try:
            with open(temp_file, 'rb') as f:
                data = {
                    'name': 'Test Dataset',
                    'description': 'A test dataset',
                    'file': (f, 'test.json')
                }
                response = client.post('/api/datasets', data=data)
            
            assert response.status_code == 201
            assert response.json['name'] == 'Test Dataset'
            assert response.json['num_samples'] == 2
        finally:
            os.unlink(temp_file)
    
    def test_get_dataset_stats(self, client):
        """Test getting dataset statistics"""
        # Create a dataset
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                {'code': 'test', 'label': 1},
                {'code': 'test2', 'label': 0}
            ], f)
            temp_file = f.name
        
        try:
            with open(temp_file, 'rb') as f:
                data = {
                    'name': 'Test Dataset',
                    'file': (f, 'test.json')
                }
                create_response = client.post('/api/datasets', data=data)
            
            dataset_id = create_response.json['id']
            
            # Get stats
            response = client.get(f'/api/datasets/{dataset_id}/stats')
            assert response.status_code == 200
            assert 'num_samples' in response.json
        finally:
            os.unlink(temp_file)


class TestTrainingAPI:
    """Test Training API endpoints"""
    
    def test_get_tasks_empty(self, client):
        """Test getting training tasks when none exist"""
        response = client.get('/api/training/tasks')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_training_task(self, client, app):
        """Test creating a training task"""
        with app.app_context():
            # Create a model and dataset first
            model = Model(name='Test Model', model_type='vulnerability_detection')
            dataset = Dataset(name='Test Dataset', format='json')
            db.session.add(model)
            db.session.add(dataset)
            db.session.commit()
            
            model_id = model.id
            dataset_id = dataset.id
        
        # Create training task
        data = {
            'name': 'Test Training',
            'model_id': model_id,
            'dataset_id': dataset_id,
            'epochs': 5
        }
        response = client.post(
            '/api/training/tasks',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.json['name'] == 'Test Training'
        assert response.json['total_epochs'] == 5
    
    def test_get_training_metrics(self, client, app):
        """Test getting training metrics"""
        with app.app_context():
            # Create necessary objects
            model = Model(name='Test Model', model_type='vulnerability_detection')
            dataset = Dataset(name='Test Dataset', format='json')
            db.session.add(model)
            db.session.add(dataset)
            db.session.commit()
            
            task = TrainingTask(
                name='Test Task',
                model_id=model.id,
                dataset_id=dataset.id,
                total_epochs=10
            )
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        
        # Get metrics
        response = client.get(f'/api/training/tasks/{task_id}/metrics')
        assert response.status_code == 200
        assert 'task' in response.json
        assert 'metrics' in response.json


class TestDatabaseModels:
    """Test database models"""
    
    def test_model_creation(self, app):
        """Test Model model"""
        with app.app_context():
            model = Model(
                name='Test Model',
                description='Test',
                version='1.0',
                model_type='vulnerability_detection'
            )
            db.session.add(model)
            db.session.commit()
            
            assert model.id is not None
            assert model.name == 'Test Model'
            assert model.created_at is not None
    
    def test_dataset_creation(self, app):
        """Test Dataset model"""
        with app.app_context():
            dataset = Dataset(
                name='Test Dataset',
                format='json',
                size=1024
            )
            db.session.add(dataset)
            db.session.commit()
            
            assert dataset.id is not None
            assert dataset.name == 'Test Dataset'
    
    def test_training_task_creation(self, app):
        """Test TrainingTask model"""
        with app.app_context():
            model = Model(name='Test Model', model_type='vulnerability_detection')
            dataset = Dataset(name='Test Dataset', format='json')
            db.session.add(model)
            db.session.add(dataset)
            db.session.commit()
            
            task = TrainingTask(
                name='Test Task',
                model_id=model.id,
                dataset_id=dataset.id,
                total_epochs=10
            )
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.model.name == 'Test Model'
            assert task.dataset.name == 'Test Dataset'
