from flask import Blueprint, request, jsonify
from datetime import datetime

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# In-memory storage for chat history (in production, use database)
chat_history = []

@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Send a message to AI and get response"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    user_message = {
        'role': 'user',
        'content': data['content'],
        'timestamp': datetime.utcnow().isoformat()
    }
    
    chat_history.append(user_message)
    
    # Generate AI response (mock implementation)
    # In production, integrate with actual AI API (Qwen, ERNIE, etc.)
    ai_response = {
        'role': 'assistant',
        'content': generate_ai_response(data['content']),
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

def generate_ai_response(user_message):
    """
    Generate AI response based on user message
    This is a mock implementation. In production, integrate with:
    - Qwen API: https://help.aliyun.com/zh/dashscope/
    - ERNIE API: https://cloud.baidu.com/doc/WENXINWORKSHOP/
    - ChatGLM API: https://open.bigmodel.cn/
    """
    message_lower = user_message.lower()
    
    # Simple keyword-based responses
    if '你好' in message_lower or 'hello' in message_lower or '您好' in message_lower:
        return "您好！我是VulWeb AI助手，很高兴为您服务。我可以帮您了解系统功能、指导操作流程。请随时向我提问！"
    
    if '帮助' in message_lower or 'help' in message_lower:
        return """我可以帮您：
1. 了解如何上传和管理模型
2. 了解如何上传和管理数据集
3. 指导创建和监控训练任务
4. 查询系统状态和统计信息
5. 解答使用过程中的问题

请告诉我您需要哪方面的帮助？"""
    
    if '模型' in message_lower:
        return """关于模型管理：

1. **上传模型**：点击"模型管理" -> "上传模型"，填写模型信息并选择模型文件
2. **支持格式**：.pkl, .pt, .pth, .h5, .onnx
3. **模型类型**：支持漏洞检测、细粒度定位等类型
4. **查看详情**：在模型列表中可以查看准确率、版本等信息

需要更详细的指导吗？"""
    
    if '数据集' in message_lower:
        return """关于数据集管理：

1. **上传数据集**：点击"数据集管理" -> "上传数据集"
2. **支持格式**：JSON, CSV, TXT, ZIP
3. **自动分析**：系统会自动分析样本数量和漏洞/安全分布
4. **统计信息**：可查看文件大小、样本数、预处理状态等

数据集格式要求请参考文档。"""
    
    if '训练' in message_lower:
        return """关于训练任务：

1. **创建任务**：选择模型和数据集，设置训练轮次
2. **实时监控**：查看训练进度、Loss、Accuracy等指标
3. **图表可视化**：使用ECharts展示训练曲线
4. **任务管理**：可以停止、删除训练任务

系统支持多任务并行训练，会自动保存训练结果。"""
    
    # Default response
    return "抱歉，我不太理解您的问题。您可以询问关于模型管理、数据集管理、训练任务等方面的问题，或者输入'帮助'查看我能提供的服务。"
