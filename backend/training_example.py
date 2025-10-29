"""
Example Training Integration

This file demonstrates how to integrate your custom training code with the VulWeb platform.
Replace the simulate_training function in backend/app/services/training_service.py with your
actual training logic following this pattern.
"""

import json
import requests
from datetime import datetime


class VulWebTrainer:
    """
    Example trainer class that integrates with VulWeb platform
    """
    
    def __init__(self, task_id, api_url='http://localhost:5000'):
        self.task_id = task_id
        self.api_url = api_url
        
    def report_metric(self, epoch, loss, accuracy, val_loss, val_accuracy, learning_rate=0.001):
        """Report training metrics to the platform"""
        try:
            response = requests.post(
                f'{self.api_url}/api/training/tasks/{self.task_id}/metrics',
                json={
                    'epoch': epoch,
                    'loss': float(loss),
                    'accuracy': float(accuracy),
                    'validation_loss': float(val_loss),
                    'validation_accuracy': float(val_accuracy),
                    'learning_rate': float(learning_rate)
                }
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error reporting metric: {e}")
            return False
    
    def train(self, model_path, dataset_path, epochs=10, batch_size=32, learning_rate=0.001):
        """
        Main training function - replace with your actual training code
        
        Args:
            model_path: Path to the model file
            dataset_path: Path to the dataset file
            epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate
        """
        print(f"Starting training for task {self.task_id}")
        print(f"Model: {model_path}")
        print(f"Dataset: {dataset_path}")
        
        # Load your dataset
        dataset = self.load_dataset(dataset_path)
        print(f"Loaded dataset with {len(dataset)} samples")
        
        # Initialize your model
        # model = YourModel()
        # optimizer = YourOptimizer(model.parameters(), lr=learning_rate)
        
        # Training loop
        for epoch in range(1, epochs + 1):
            print(f"\nEpoch {epoch}/{epochs}")
            
            # Training phase
            # train_loss, train_acc = self.train_epoch(model, dataset, optimizer)
            
            # Validation phase
            # val_loss, val_acc = self.validate(model, dataset)
            
            # For demonstration, using simulated metrics
            train_loss = 1.0 - (epoch / epochs) * 0.8
            train_acc = 0.5 + (epoch / epochs) * 0.4
            val_loss = train_loss + 0.05
            val_acc = train_acc - 0.05
            
            print(f"Loss: {train_loss:.4f}, Accuracy: {train_acc:.4f}")
            print(f"Val Loss: {val_loss:.4f}, Val Accuracy: {val_acc:.4f}")
            
            # Report to platform
            self.report_metric(
                epoch=epoch,
                loss=train_loss,
                accuracy=train_acc,
                val_loss=val_loss,
                val_accuracy=val_acc,
                learning_rate=learning_rate
            )
        
        print(f"\nTraining completed for task {self.task_id}")
        return True
    
    def load_dataset(self, dataset_path):
        """Load dataset from file"""
        with open(dataset_path, 'r') as f:
            if dataset_path.endswith('.json'):
                return json.load(f)
            # Add more format handlers as needed
        return []
    
    def train_epoch(self, model, dataset, optimizer):
        """Train for one epoch - implement your training logic"""
        # Your training code here
        pass
    
    def validate(self, model, dataset):
        """Validate the model - implement your validation logic"""
        # Your validation code here
        pass


# Example usage in training_service.py
def start_training_task(task_id, config):
    """
    Integration point in backend/app/services/training_service.py
    """
    from ..models import db, TrainingTask
    
    task = TrainingTask.query.get(task_id)
    if not task:
        raise Exception("Task not found")
    
    # Initialize trainer
    trainer = VulWebTrainer(task_id)
    
    # Start training
    try:
        trainer.train(
            model_path=task.model.file_path,
            dataset_path=task.dataset.file_path,
            epochs=config.get('epochs', 10),
            batch_size=config.get('batch_size', 32),
            learning_rate=config.get('learning_rate', 0.001)
        )
        
        # Update task status
        task.status = 'completed'
        task.end_time = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.end_time = datetime.utcnow()
        db.session.commit()
        raise


# Standalone script example
if __name__ == '__main__':
    """
    You can also run training as a standalone script
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python training_example.py <task_id>")
        sys.exit(1)
    
    task_id = int(sys.argv[1])
    
    # Fetch task details from API
    response = requests.get(f'http://localhost:5000/api/training/tasks/{task_id}')
    if response.status_code != 200:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)
    
    task_data = response.json()
    
    # Get model and dataset info
    model_response = requests.get(f'http://localhost:5000/api/models/{task_data["model_id"]}')
    dataset_response = requests.get(f'http://localhost:5000/api/datasets/{task_data["dataset_id"]}')
    
    model_data = model_response.json()
    dataset_data = dataset_response.json()
    
    # Initialize and run trainer
    trainer = VulWebTrainer(task_id)
    trainer.train(
        model_path=model_data['file_path'],
        dataset_path=dataset_data['file_path'],
        epochs=task_data['total_epochs']
    )
