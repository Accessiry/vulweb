"""
Chat API - WebSocket and REST endpoints for AI chat functionality
"""
from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room
from ..services.ai_service import ai_service

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/message', methods=['POST'])
def send_message():
    """REST endpoint for sending chat messages"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    message = data['message']
    session_id = data.get('session_id', 'default')
    
    try:
        # Process message through AI service
        result = ai_service.process_message(message, session_id)
        return jsonify(result), 200 if result['success'] else 500
    except Exception:
        # Log the actual error internally but don't expose details to user
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your message. Please try again.',
            'response': {
                'type': 'error',
                'content': 'Sorry, I encountered an error. Please try again.'
            }
        }), 500


@chat_bp.route('/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    session_id = request.args.get('session_id', 'default')
    limit = request.args.get('limit', type=int)
    
    history = ai_service.get_conversation_history(session_id, limit)
    
    return jsonify({
        'success': True,
        'history': history
    }), 200


@chat_bp.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    data = request.get_json()
    session_id = data.get('session_id', 'default') if data else 'default'
    
    ai_service.clear_context(session_id)
    
    return jsonify({
        'success': True,
        'message': 'Conversation history cleared'
    }), 200


# WebSocket event handlers (to be registered with SocketIO in __init__.py)
def register_socketio_handlers(socketio):
    """Register WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print('Client connected')
        emit('connected', {'message': 'Connected to AI chat server'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print('Client disconnected')
    
    @socketio.on('join')
    def handle_join(data):
        """Handle client joining a room (session)"""
        session_id = data.get('session_id', 'default')
        join_room(session_id)
        emit('joined', {'session_id': session_id}, room=session_id)
    
    @socketio.on('leave')
    def handle_leave(data):
        """Handle client leaving a room"""
        session_id = data.get('session_id', 'default')
        leave_room(session_id)
        emit('left', {'session_id': session_id}, room=session_id)
    
    @socketio.on('chat_message')
    def handle_message(data):
        """Handle incoming chat message"""
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            emit('error', {'error': 'Message is required'})
            return
        
        # Process message through AI service
        result = ai_service.process_message(message, session_id)
        
        # Emit response back to client
        emit('chat_response', result, room=session_id)
    
    @socketio.on('clear_history')
    def handle_clear_history(data):
        """Handle clear history request"""
        session_id = data.get('session_id', 'default')
        ai_service.clear_context(session_id)
        emit('history_cleared', {'session_id': session_id}, room=session_id)
