"""
Tests for AI Chat API
"""
import pytest
import json
from app import create_app, socketio
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


@pytest.fixture
def socketio_client(app):
    """Create SocketIO test client"""
    return socketio.test_client(app)


class TestChatAPI:
    """Test Chat REST API endpoints"""
    
    def test_send_message(self, client):
        """Test sending a chat message"""
        data = {
            'message': 'Hello',
            'session_id': 'test_session'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['success'] is True
        assert 'response' in response.json
    
    def test_send_message_without_content(self, client):
        """Test sending empty message"""
        data = {}
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_get_history(self, client):
        """Test getting conversation history"""
        # Send a message first
        data = {
            'message': 'Test message',
            'session_id': 'test_session'
        }
        client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Get history
        response = client.get('/api/chat/history?session_id=test_session')
        assert response.status_code == 200
        assert response.json['success'] is True
        assert len(response.json['history']) >= 2  # User message + assistant response
    
    def test_clear_history(self, client):
        """Test clearing conversation history"""
        # Send a message first
        data = {
            'message': 'Test message',
            'session_id': 'test_session'
        }
        client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Clear history
        response = client.post(
            '/api/chat/clear',
            data=json.dumps({'session_id': 'test_session'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json['success'] is True


class TestAIAgents:
    """Test AI Agent functionality"""
    
    def test_model_agent_list_models(self, client, app):
        """Test model agent listing models"""
        with app.app_context():
            # Create test models
            model1 = Model(name='Model 1', model_type='vulnerability_detection', accuracy=0.95)
            model2 = Model(name='Model 2', model_type='vulnerability_detection', accuracy=0.88)
            db.session.add(model1)
            db.session.add(model2)
            db.session.commit()
        
        data = {
            'message': 'Show all models',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'Model 1' in response.json['response']['content']
        assert 'Model 2' in response.json['response']['content']
    
    def test_model_agent_filter_by_accuracy(self, client, app):
        """Test model agent filtering by accuracy"""
        with app.app_context():
            model1 = Model(name='High Accuracy', model_type='vulnerability_detection', accuracy=0.95)
            model2 = Model(name='Low Accuracy', model_type='vulnerability_detection', accuracy=0.85)
            db.session.add(model1)
            db.session.add(model2)
            db.session.commit()
        
        data = {
            'message': 'Show models with accuracy greater than 90%',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'High Accuracy' in response.json['response']['content']
        assert 'Low Accuracy' not in response.json['response']['content']
    
    def test_dataset_agent_list_datasets(self, client, app):
        """Test dataset agent listing datasets"""
        with app.app_context():
            dataset1 = Dataset(name='Dataset 1', format='json', num_samples=100)
            dataset2 = Dataset(name='Dataset 2', format='csv', num_samples=200)
            db.session.add(dataset1)
            db.session.add(dataset2)
            db.session.commit()
        
        data = {
            'message': 'List all datasets',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'Dataset 1' in response.json['response']['content']
        assert 'Dataset 2' in response.json['response']['content']
    
    def test_training_agent_show_tasks(self, client, app):
        """Test training agent showing tasks"""
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
                status='running',
                progress=50,
                total_epochs=10
            )
            db.session.add(task)
            db.session.commit()
        
        data = {
            'message': 'Show all training tasks',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'Test Task' in response.json['response']['content']
    
    def test_analysis_agent_statistics(self, client, app):
        """Test analysis agent showing statistics"""
        with app.app_context():
            model = Model(name='Test Model', model_type='vulnerability_detection')
            dataset = Dataset(name='Test Dataset', format='json')
            db.session.add(model)
            db.session.add(dataset)
            db.session.commit()
        
        data = {
            'message': 'Show platform statistics',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'Platform Statistics' in response.json['response']['content']
        assert 'Total Models' in response.json['response']['content']
    
    def test_system_assistant_help(self, client):
        """Test system assistant providing help"""
        data = {
            'message': 'What file formats are supported?',
            'session_id': 'test'
        }
        response = client.post(
            '/api/chat/message',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'format' in response.json['response']['content'].lower()


class TestWebSocketChat:
    """Test WebSocket chat functionality"""
    
    def test_connect(self, socketio_client):
        """Test WebSocket connection"""
        assert socketio_client.is_connected()
    
    # Note: WebSocket event tests can be flaky in test environment
    # These are better tested through integration/E2E tests
