from flask import Blueprint, request, jsonify
from datetime import datetime
from ..services.rag_service import get_rag_service
from ..models import Model, Dataset, TrainingTask

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# In-memory storage for chat history (in production, use database)
chat_history = []

@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Send a message to AI and get response using RAG"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    user_message = {
        'role': 'user',
        'content': data['content'],
        'timestamp': datetime.utcnow().isoformat()
    }
    
    chat_history.append(user_message)
    
    # Get system context
    try:
        models = [m.to_dict() for m in Model.query.all()]
        datasets = [d.to_dict() for d in Dataset.query.all()]
        tasks = [t.to_dict() for t in TrainingTask.query.all()]
        
        context = {
            'models': models,
            'datasets': datasets,
            'tasks': tasks
        }
    except Exception as e:
        # If database query fails, continue with empty context
        print(f"Warning: Failed to fetch system context: {e}")
        context = {}
    
    # Get LLM configuration from request (optional)
    llm_config = data.get('llm_config', None)
    use_llm = data.get('use_llm', False)
    
    # Generate AI response using RAG service
    rag_service = get_rag_service()
    ai_content = rag_service.generate_response(
        query=data['content'],
        context=context,
        use_llm=use_llm,
        llm_config=llm_config
    )
    
    ai_response = {
        'role': 'assistant',
        'content': ai_content,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    chat_history.append(ai_response)
    
    return jsonify(ai_response), 200

@chat_bp.route('/history', methods=['GET'])
def get_history():
    """Get chat history"""
    return jsonify(chat_history), 200

@chat_bp.route('/history', methods=['DELETE'])
def clear_history():
    """Clear chat history"""
    chat_history.clear()
    return jsonify({'message': 'Chat history cleared'}), 200

@chat_bp.route('/config', methods=['POST'])
def update_config():
    """Update AI configuration (LLM settings)"""
    data = request.get_json()
    
    # In production, save to database or config file
    # For now, just validate the configuration
    required_fields = ['provider', 'api_key']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Test the configuration
    rag_service = get_rag_service()
    try:
        test_response = rag_service.generate_response(
            query="测试连接",
            use_llm=True,
            llm_config=data
        )
        return jsonify({
            'message': 'Configuration validated successfully',
            'test_response': test_response
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Configuration test failed: {str(e)}'
        }), 400

@chat_bp.route('/knowledge-base/reload', methods=['POST'])
def reload_knowledge_base():
    """Reload knowledge base (admin endpoint)"""
    try:
        rag_service = get_rag_service()
        rag_service.reload_knowledge_base()
        return jsonify({'message': 'Knowledge base reloaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to reload knowledge base: {str(e)}'}), 500
