"""
AI Service Module - Manages AI agents and conversation handling
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from flask import current_app


class ConversationContext:
    """Manages conversation context and history"""
    
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.metadata: Dict[str, Any] = {}
        
    def add_message(self, role: str, content: str):
        """Add a message to context"""
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation messages"""
        if limit:
            return self.messages[-limit:]
        return self.messages
        
    def clear(self):
        """Clear conversation context"""
        self.messages = []
        self.metadata = {}
        
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'messages': self.messages,
            'metadata': self.metadata
        }


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name: str, description: str, capabilities: List[str]):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        
    def can_handle(self, message: str, context: ConversationContext) -> bool:
        """Check if this agent can handle the message"""
        # Default implementation - can be overridden
        message_lower = message.lower()
        for capability in self.capabilities:
            if capability.lower() in message_lower:
                return True
        return False
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process a user message and return a response"""
        raise NotImplementedError("Subclasses must implement process_message")
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        return f"You are {self.name}. {self.description}"


class ModelManagementAgent(BaseAgent):
    """Agent for managing ML models"""
    
    def __init__(self):
        super().__init__(
            name="Model Management Agent",
            description="I help you manage machine learning models - upload, view, update, delete, and compare models.",
            capabilities=[
                'model', 'models', 'upload model', 'delete model', 
                'show models', 'compare models', 'accuracy', 'performance'
            ]
        )
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process model-related queries"""
        from ..models import Model
        
        message_lower = message.lower()
        
        # Filter models by accuracy first (more specific)
        if 'accuracy' in message_lower and any(op in message_lower for op in ['greater', '>', 'above', 'more than']):
            try:
                # Extract accuracy threshold
                import re
                numbers = re.findall(r'\d+(?:\.\d+)?', message)
                if numbers:
                    threshold = float(numbers[0]) / 100 if float(numbers[0]) > 1 else float(numbers[0])
                    models = Model.query.filter(Model.accuracy >= threshold).all()
                    if models:
                        model_list = [f"- {m.name} (Accuracy: {m.accuracy:.2%})" for m in models]
                        return {
                            'type': 'text',
                            'content': f"Models with accuracy >= {threshold:.0%}:\n" + "\n".join(model_list),
                            'data': {'models': [m.to_dict() for m in models]}
                        }
                    else:
                        return {
                            'type': 'text',
                            'content': f"No models found with accuracy >= {threshold:.0%}."
                        }
            except Exception as e:
                return {
                    'type': 'text',
                    'content': f"I had trouble understanding the accuracy threshold. Could you rephrase?"
                }
        
        # Get all models intent
        if any(phrase in message_lower for phrase in ['show all', 'list all', 'get all', 'show models', 'list models']):
            models = Model.query.all()
            if models:
                model_list = [f"- {m.name} (Type: {m.model_type}, Accuracy: {m.accuracy or 'N/A'})" for m in models]
                return {
                    'type': 'text',
                    'content': f"Here are all the models:\n" + "\n".join(model_list),
                    'data': {'models': [m.to_dict() for m in models]}
                }
            else:
                return {
                    'type': 'text',
                    'content': "No models found. Would you like to upload a model?"
                }
        
        # Default response
        return {
            'type': 'text',
            'content': "I can help you with:\n- Listing all models\n- Filtering models by accuracy\n- Uploading new models\n- Comparing model performance\n\nWhat would you like to do?"
        }


class DatasetManagementAgent(BaseAgent):
    """Agent for managing datasets"""
    
    def __init__(self):
        super().__init__(
            name="Dataset Management Agent",
            description="I help you manage datasets - upload, view statistics, analyze, and preprocess datasets.",
            capabilities=[
                'dataset', 'datasets', 'data', 'upload dataset', 
                'show datasets', 'statistics', 'preprocess'
            ]
        )
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process dataset-related queries"""
        from ..models import Dataset
        
        message_lower = message.lower()
        
        # List all datasets
        if any(phrase in message_lower for phrase in ['show all', 'list all', 'get all', 'show datasets', 'list datasets']):
            datasets = Dataset.query.all()
            if datasets:
                dataset_list = [
                    f"- {d.name} (Format: {d.format}, Samples: {d.num_samples or 'N/A'})" 
                    for d in datasets
                ]
                return {
                    'type': 'text',
                    'content': f"Here are all the datasets:\n" + "\n".join(dataset_list),
                    'data': {'datasets': [d.to_dict() for d in datasets]}
                }
            else:
                return {
                    'type': 'text',
                    'content': "No datasets found. Would you like to upload a dataset?"
                }
        
        # Find dataset with most samples
        if 'most' in message_lower and any(word in message_lower for word in ['samples', 'vulnerable', 'data']):
            datasets = Dataset.query.filter(Dataset.num_samples.isnot(None)).order_by(Dataset.num_samples.desc()).first()
            if datasets:
                return {
                    'type': 'text',
                    'content': f"The dataset with the most samples is '{datasets.name}' with {datasets.num_samples} samples."
                }
            else:
                return {
                    'type': 'text',
                    'content': "No datasets with sample information found."
                }
        
        # Default response
        return {
            'type': 'text',
            'content': "I can help you with:\n- Listing all datasets\n- Viewing dataset statistics\n- Finding datasets with specific criteria\n- Analyzing dataset contents\n\nWhat would you like to do?"
        }


class TrainingAgent(BaseAgent):
    """Agent for managing training tasks"""
    
    def __init__(self):
        super().__init__(
            name="Training Agent",
            description="I help you manage training tasks - start, stop, monitor progress, and view training metrics.",
            capabilities=[
                'train', 'training', 'start training', 'stop training',
                'training progress', 'training status', 'metrics', 'loss', 'epoch'
            ]
        )
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process training-related queries"""
        from ..models import TrainingTask
        
        message_lower = message.lower()
        
        # Show all training tasks
        if any(phrase in message_lower for phrase in ['show all', 'list all', 'show tasks', 'list tasks', 'training tasks']):
            tasks = TrainingTask.query.all()
            if tasks:
                task_list = [
                    f"- {t.name} (Status: {t.status}, Progress: {t.progress or 0}%)" 
                    for t in tasks
                ]
                return {
                    'type': 'text',
                    'content': f"Here are all the training tasks:\n" + "\n".join(task_list),
                    'data': {'tasks': [t.to_dict() for t in tasks]}
                }
            else:
                return {
                    'type': 'text',
                    'content': "No training tasks found. Would you like to start a new training task?"
                }
        
        # Show running tasks
        if 'running' in message_lower or 'active' in message_lower:
            tasks = TrainingTask.query.filter_by(status='running').all()
            if tasks:
                task_list = [f"- {t.name} (Progress: {t.progress or 0}%)" for t in tasks]
                return {
                    'type': 'text',
                    'content': f"Running training tasks:\n" + "\n".join(task_list),
                    'data': {'tasks': [t.to_dict() for t in tasks]}
                }
            else:
                return {
                    'type': 'text',
                    'content': "No running training tasks."
                }
        
        # Default response
        return {
            'type': 'text',
            'content': "I can help you with:\n- Starting new training tasks\n- Monitoring training progress\n- Viewing training metrics\n- Stopping running tasks\n\nWhat would you like to do?"
        }


class DataAnalysisAgent(BaseAgent):
    """Agent for data analysis and reporting"""
    
    def __init__(self):
        super().__init__(
            name="Data Analysis Agent",
            description="I help you analyze data, generate reports, and create visualizations.",
            capabilities=[
                'analyze', 'analysis', 'report', 'statistics', 'stats', 'trends',
                'visualization', 'chart', 'graph', 'compare', 'platform', 'overview'
            ]
        )
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process analysis-related queries"""
        from ..models import Model, Dataset, TrainingTask
        
        message_lower = message.lower()
        
        # Platform statistics
        if 'statistics' in message_lower or 'stats' in message_lower or 'overview' in message_lower:
            model_count = Model.query.count()
            dataset_count = Dataset.query.count()
            task_count = TrainingTask.query.count()
            running_tasks = TrainingTask.query.filter_by(status='running').count()
            
            return {
                'type': 'text',
                'content': f"""Platform Statistics:
- Total Models: {model_count}
- Total Datasets: {dataset_count}
- Total Training Tasks: {task_count}
- Running Tasks: {running_tasks}""",
                'data': {
                    'models': model_count,
                    'datasets': dataset_count,
                    'tasks': task_count,
                    'running_tasks': running_tasks
                }
            }
        
        # Best performing model
        if 'best' in message_lower and 'model' in message_lower:
            model = Model.query.filter(Model.accuracy.isnot(None)).order_by(Model.accuracy.desc()).first()
            if model:
                return {
                    'type': 'text',
                    'content': f"The best performing model is '{model.name}' with {model.accuracy:.2%} accuracy.",
                    'data': {'model': model.to_dict()}
                }
            else:
                return {
                    'type': 'text',
                    'content': "No models with accuracy metrics found."
                }
        
        # Default response
        return {
            'type': 'text',
            'content': "I can help you with:\n- Platform statistics\n- Model performance analysis\n- Training trend analysis\n- Generating comparison reports\n\nWhat would you like to analyze?"
        }


class SystemAssistantAgent(BaseAgent):
    """Agent for system help and guidance"""
    
    def __init__(self):
        super().__init__(
            name="System Assistant",
            description="I provide help with platform usage, answer questions, and troubleshoot issues.",
            capabilities=[
                'help', 'how to', 'what is', 'can i', 'support',
                'format', 'error', 'problem', 'issue', 'guide'
            ]
        )
        
    def process_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Process help and guidance queries"""
        message_lower = message.lower()
        
        # Supported formats
        if 'format' in message_lower and 'support' in message_lower:
            return {
                'type': 'text',
                'content': """Supported file formats:
                
**Models:**
- .pkl (Pickle)
- .pt, .pth (PyTorch)
- .h5 (Keras/TensorFlow)

**Datasets:**
- .json (JSON)
- .csv (CSV)
- .txt (Text)
- .zip (Compressed archives)

You can upload files through the respective pages or ask me to help you!"""
            }
        
        # How to upload model
        if 'how' in message_lower and 'upload' in message_lower and 'model' in message_lower:
            return {
                'type': 'text',
                'content': """To upload a model:

1. Go to the Models page
2. Click the "Add Model" button
3. Fill in the model information (name, description, version, type)
4. Upload your model file (.pkl, .pt, .pth, or .h5)
5. Click "Create Model"

Or just tell me the details and I can help guide you through the process!"""
            }
        
        # How to start training
        if 'how' in message_lower and 'train' in message_lower:
            return {
                'type': 'text',
                'content': """To start training:

1. Make sure you have both a model and dataset uploaded
2. Go to the Training page
3. Click "Start Training"
4. Enter a task name
5. Select your model and dataset
6. Set the number of epochs
7. Click "Start Training"

The training will run in the background and you can monitor progress in real-time!"""
            }
        
        # Default help
        return {
            'type': 'text',
            'content': """I'm here to help! I can assist with:

- Platform features and how to use them
- Supported file formats
- Troubleshooting issues
- Best practices for model training
- Integration guidance

What would you like to know?"""
        }


class AgentRouter:
    """Routes messages to appropriate agents"""
    
    def __init__(self):
        # Order matters - more specific agents first
        self.agents = [
            DataAnalysisAgent(),      # Check for platform stats first
            ModelManagementAgent(),
            DatasetManagementAgent(),
            TrainingAgent(),
            SystemAssistantAgent()
        ]
        
    def route_message(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Route message to the most appropriate agent"""
        # Find the best matching agent
        for agent in self.agents:
            if agent.can_handle(message, context):
                return agent.process_message(message, context)
        
        # If no specific agent matches, use system assistant as fallback
        return self.agents[-1].process_message(message, context)


class AIService:
    """Main AI service that coordinates agents and handles conversations"""
    
    def __init__(self):
        self.router = AgentRouter()
        self.contexts: Dict[str, ConversationContext] = {}
        
    def get_or_create_context(self, session_id: str) -> ConversationContext:
        """Get or create a conversation context for a session"""
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext()
        return self.contexts[session_id]
        
    def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """Process a user message and return a response"""
        context = self.get_or_create_context(session_id)
        context.add_message('user', message)
        
        try:
            # Route to appropriate agent
            response = self.router.route_message(message, context)
            
            # Add assistant response to context
            context.add_message('assistant', response.get('content', ''))
            
            return {
                'success': True,
                'response': response,
                'context': {
                    'message_count': len(context.messages)
                }
            }
        except Exception as e:
            error_msg = f"I encountered an error processing your request: {str(e)}"
            context.add_message('assistant', error_msg)
            return {
                'success': False,
                'error': str(e),
                'response': {
                    'type': 'text',
                    'content': error_msg
                }
            }
    
    def clear_context(self, session_id: str):
        """Clear conversation context for a session"""
        if session_id in self.contexts:
            self.contexts[session_id].clear()
            
    def get_conversation_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history for a session"""
        context = self.get_or_create_context(session_id)
        return context.get_messages(limit)


# Global AI service instance
ai_service = AIService()
