# AI Chat Integration Guide

## Overview

VulWeb now includes an intelligent AI chat assistant that allows users to interact with the platform using natural language. The chat system features a multi-agent architecture where specialized agents handle different aspects of the platform.

## Features

### 🤖 Multi-Agent System

The AI system consists of 5 specialized agents:

1. **Model Management Agent**
   - List and filter models
   - View model performance metrics
   - Compare models
   - Example: "Show models with accuracy greater than 90%"

2. **Dataset Management Agent**
   - List and analyze datasets
   - View dataset statistics
   - Find datasets by criteria
   - Example: "Show all datasets"

3. **Training Agent**
   - Monitor training tasks
   - View training progress
   - Check task status
   - Example: "Show running training tasks"

4. **Data Analysis Agent**
   - Platform statistics
   - Performance analysis
   - Generate reports
   - Example: "Show platform statistics"

5. **System Assistant Agent**
   - Platform help and guidance
   - Answer usage questions
   - Troubleshooting support
   - Example: "What file formats are supported?"

### 💬 Chat Interface

- **Floating Widget**: Elegant floating chat button in the bottom-right corner
- **Real-time Communication**: WebSocket-based for instant responses
- **Message History**: Persistent conversation history
- **Typing Indicators**: Visual feedback when AI is processing
- **Suggested Queries**: Quick-start buttons for common questions
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Automatic dark mode support

## Usage

### Basic Interaction

1. Click the chat button (💬) in the bottom-right corner
2. Type your question or select a suggested query
3. Press Enter or click the send button
4. The AI will respond with relevant information

### Example Queries

**Model Management:**
```
- Show all models
- List models with accuracy above 85%
- What is the best performing model?
- Compare model performance
```

**Dataset Management:**
```
- Show all datasets
- Which dataset has the most samples?
- Display dataset statistics
- List available datasets
```

**Training Tasks:**
```
- Show all training tasks
- List running tasks
- Show training progress
- What tasks are active?
```

**Platform Analysis:**
```
- Show platform statistics
- What's the overall platform status?
- Generate a summary report
- How many models do we have?
```

**Help & Support:**
```
- What file formats are supported?
- How do I upload a model?
- How do I start training?
- Guide me through the platform
```

## API Reference

### REST API Endpoints

#### Send Message
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Show all models",
  "session_id": "user_session_123"
}
```

Response:
```json
{
  "success": true,
  "response": {
    "type": "text",
    "content": "Here are all the models:\n- Model 1 (Accuracy: 95%)\n- Model 2 (Accuracy: 88%)",
    "data": {
      "models": [...]
    }
  },
  "context": {
    "message_count": 2
  }
}
```

#### Get History
```http
GET /api/chat/history?session_id=user_session_123&limit=10
```

Response:
```json
{
  "success": true,
  "history": [
    {
      "role": "user",
      "content": "Show all models",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Here are all the models...",
      "timestamp": "2024-01-01T12:00:01Z"
    }
  ]
}
```

#### Clear History
```http
POST /api/chat/clear
Content-Type: application/json

{
  "session_id": "user_session_123"
}
```

### WebSocket Events

#### Connect
```javascript
socket.on('connect', () => {
  console.log('Connected to chat server');
});
```

#### Join Session
```javascript
socket.emit('join', { session_id: 'user_session_123' });
```

#### Send Message
```javascript
socket.emit('chat_message', {
  message: 'Show all models',
  session_id: 'user_session_123'
});
```

#### Receive Response
```javascript
socket.on('chat_response', (data) => {
  console.log('AI Response:', data.response.content);
});
```

#### Clear History
```javascript
socket.emit('clear_history', { session_id: 'user_session_123' });
```

## Frontend Integration

### Using the ChatWidget Component

The ChatWidget is automatically included in the main App component:

```javascript
import ChatWidget from './components/ChatWidget';

function App() {
  return (
    <div className="app">
      {/* Your app content */}
      <ChatWidget />
    </div>
  );
}
```

### Customizing the Chat Widget

You can customize the chat widget by modifying `ChatWidget.css`:

```css
/* Change chat button colors */
.chat-button {
  background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
}

/* Adjust widget size */
.chat-widget {
  width: 400px;
  height: 600px;
}
```

## Backend Development

### Creating a New Agent

To add a new specialized agent:

```python
from app.services.ai_service import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Custom Agent",
            description="Handles custom operations",
            capabilities=['custom', 'special', 'keywords']
        )
    
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        # Your logic here
        return {
            'type': 'text',
            'content': 'Your response'
        }
```

Register the agent in `AgentRouter`:

```python
class AgentRouter:
    def __init__(self):
        self.agents = [
            CustomAgent(),  # Add your agent
            ModelManagementAgent(),
            # ... other agents
        ]
```

### Agent Response Types

Agents can return different response types:

```python
# Text response
{
    'type': 'text',
    'content': 'Response text'
}

# Error response
{
    'type': 'error',
    'content': 'Error message'
}

# Response with data
{
    'type': 'text',
    'content': 'Summary text',
    'data': {
        'models': [...],
        'count': 5
    }
}
```

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# AI Configuration (optional - for OpenAI integration)
OPENAI_API_KEY=your_openai_key
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000

# WebSocket Configuration
SOCKETIO_CORS_ALLOWED_ORIGINS=*
```

### Docker Configuration

The docker-compose.yml already includes the necessary configuration:

```yaml
backend:
  environment:
    - SOCKETIO_CORS_ALLOWED_ORIGINS=*
```

## Testing

### Backend Tests

Run the chat API tests:

```bash
cd backend
pytest tests/test_chat.py -v
```

### Frontend Tests

Test the chat component:

```bash
cd frontend
npm test -- ChatWidget
```

### Manual Testing

1. Start the backend: `cd backend && python run.py`
2. Start the frontend: `cd frontend && npm start`
3. Open http://localhost:3000
4. Click the chat button and test queries

## Troubleshooting

### Chat Button Not Appearing

- Check that ChatWidget is imported in App.js
- Verify CSS is loaded properly
- Check browser console for errors

### WebSocket Connection Issues

- Ensure backend is running on correct port (5000)
- Check CORS settings in backend config
- Verify REACT_APP_SOCKET_URL environment variable
- Check browser console for connection errors

### Messages Not Sending

- Check WebSocket connection status
- Verify REST API fallback is working
- Check network tab in browser dev tools
- Review backend logs for errors

### Agent Not Responding Correctly

- Check agent capability keywords
- Review agent routing logic
- Verify database queries are working
- Check backend logs for exceptions

## Performance Considerations

### Connection Management

- WebSocket connections are automatically managed
- Fallback to REST API if WebSocket unavailable
- Connections are cleaned up on component unmount

### Message History

- History is limited to last 10 messages by default
- Adjust limit in API calls as needed
- Consider pagination for large histories

### Scalability

- WebSocket connections use minimal resources
- Agent processing is lightweight
- Database queries are optimized
- Consider Redis for session storage in production

## Security

### Input Validation

- All user inputs are validated
- SQL injection protection via SQLAlchemy
- XSS protection in React

### Session Management

- Session IDs used for conversation isolation
- No sensitive data stored in conversations
- Clear history option available

### CORS Configuration

- Configure CORS properly for production
- Restrict WebSocket origins in production
- Use environment variables for configuration

## Future Enhancements

Potential features for future development:

1. **Voice Input/Output**: Web Speech API integration
2. **Rich Media**: Image and chart generation
3. **Action Confirmations**: Interactive confirmation dialogs
4. **Smart Suggestions**: Context-aware query suggestions
5. **Multi-language**: Internationalization support
6. **Workflow Automation**: Complex task automation
7. **Analytics**: Chat interaction analytics
8. **Personalization**: User preference learning

## Support

For issues or questions:

- Create an issue on GitHub
- Check the main README.md
- Review test files for examples
- Contact: support@vulweb.com

## License

Same as the main project - MIT License
