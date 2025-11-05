"""
Tests for RAG service
"""
import pytest
import os
import json
from app import create_app
from app.models import db
from app.services.rag_service import RAGService, get_rag_service


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


class TestRAGService:
    """Test RAG Service functionality"""
    
    def test_rag_service_initialization(self):
        """Test RAG service can be initialized"""
        rag_service = RAGService()
        assert rag_service is not None
        assert rag_service.knowledge_base_path is not None
    
    def test_get_rag_service_singleton(self):
        """Test global RAG service instance"""
        service1 = get_rag_service()
        service2 = get_rag_service()
        assert service1 is service2
    
    def test_retrieve_relevant_docs(self):
        """Test document retrieval"""
        rag_service = get_rag_service()
        
        # Test with model-related query
        docs = rag_service.retrieve_relevant_docs("如何上传模型", n_results=2)
        assert isinstance(docs, list)
        # May be empty if embedding model not loaded
        if docs:
            assert len(docs) <= 2
            assert 'content' in docs[0]
    
    def test_generate_response_without_llm(self):
        """Test response generation without LLM"""
        rag_service = get_rag_service()
        
        # Test basic query
        response = rag_service.generate_response(
            query="如何上传模型",
            use_llm=False
        )
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_generate_response_with_context(self):
        """Test response generation with system context"""
        rag_service = get_rag_service()
        
        context = {
            'models': [{'id': 1, 'name': 'Test Model'}],
            'datasets': [{'id': 1, 'name': 'Test Dataset'}],
            'tasks': [{'id': 1, 'status': 'running'}]
        }
        
        response = rag_service.generate_response(
            query="系统有多少个模型",
            context=context,
            use_llm=False
        )
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_greeting_response(self):
        """Test greeting response"""
        rag_service = get_rag_service()
        
        response = rag_service.generate_response(
            query="你好",
            use_llm=False
        )
        assert isinstance(response, str)
        assert '助手' in response or '您好' in response
    
    def test_help_response(self):
        """Test help response"""
        rag_service = get_rag_service()
        
        response = rag_service.generate_response(
            query="帮助",
            use_llm=False
        )
        assert isinstance(response, str)
        assert len(response) > 0


class TestChatAPI:
    """Test Chat API with RAG integration"""
    
    def test_send_message(self, client):
        """Test sending a message"""
        response = client.post(
            '/api/chat/message',
            json={'content': '你好'}
        )
        assert response.status_code == 200
        data = response.json
        assert data['role'] == 'assistant'
        assert 'content' in data
        assert 'timestamp' in data
    
    def test_send_message_without_content(self, client):
        """Test sending message without content"""
        response = client.post('/api/chat/message', json={})
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_get_chat_history(self, client):
        """Test getting chat history"""
        # Send a message first
        client.post('/api/chat/message', json={'content': '测试消息'})
        
        # Get history
        response = client.get('/api/chat/history')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) >= 2  # User message + AI response
    
    def test_clear_chat_history(self, client):
        """Test clearing chat history"""
        # Send a message
        client.post('/api/chat/message', json={'content': '测试消息'})
        
        # Clear history
        response = client.delete('/api/chat/history')
        assert response.status_code == 200
        
        # Verify history is empty
        history_response = client.get('/api/chat/history')
        assert len(history_response.json) == 0
    
    def test_reload_knowledge_base(self, client):
        """Test reloading knowledge base"""
        response = client.post('/api/chat/knowledge-base/reload')
        assert response.status_code == 200
        assert 'message' in response.json
    
    def test_message_with_model_query(self, client):
        """Test message asking about models"""
        response = client.post(
            '/api/chat/message',
            json={'content': '如何上传模型？'}
        )
        assert response.status_code == 200
        data = response.json
        # Should return a response (might be fallback or KB-based)
        assert len(data['content']) > 0
    
    def test_message_with_dataset_query(self, client):
        """Test message asking about datasets"""
        response = client.post(
            '/api/chat/message',
            json={'content': '数据集格式要求是什么？'}
        )
        assert response.status_code == 200
        data = response.json
        # Should return a response
        assert len(data['content']) > 0
    
    def test_message_with_training_query(self, client):
        """Test message asking about training"""
        response = client.post(
            '/api/chat/message',
            json={'content': '如何创建训练任务？'}
        )
        assert response.status_code == 200
        data = response.json
        # Should return a response
        assert len(data['content']) > 0
