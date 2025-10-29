from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from ..models import db, TrainingTask, TrainingMetric, Model, Dataset
from ..services.training_service import start_training_task

training_bp = Blueprint('training', __name__, url_prefix='/api/training')

@training_bp.route('/tasks', methods=['GET'])
def get_training_tasks():
    """Get all training tasks"""
    tasks = TrainingTask.query.order_by(TrainingTask.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@training_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_training_task(task_id):
    """Get a specific training task"""
    task = TrainingTask.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@training_bp.route('/tasks', methods=['POST'])
def create_training_task():
    """Create and start a new training task"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Task name is required'}), 400
    if not data.get('model_id'):
        return jsonify({'error': 'Model ID is required'}), 400
    if not data.get('dataset_id'):
        return jsonify({'error': 'Dataset ID is required'}), 400
    
    # Verify model and dataset exist
    model = Model.query.get(data['model_id'])
    if not model:
        return jsonify({'error': 'Model not found'}), 404
    
    dataset = Dataset.query.get(data['dataset_id'])
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
    
    task = TrainingTask(
        name=data.get('name'),
        model_id=data['model_id'],
        dataset_id=data['dataset_id'],
        status='pending',
        total_epochs=data.get('epochs', 10)
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Start training asynchronously
    try:
        start_training_task(task.id, data)
        task.status = 'running'
        task.start_time = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        db.session.commit()
        current_app.logger.error(f"Failed to start training: {str(e)}")
    
    return jsonify(task.to_dict()), 201

@training_bp.route('/tasks/<int:task_id>/stop', methods=['POST'])
def stop_training_task(task_id):
    """Stop a running training task"""
    task = TrainingTask.query.get_or_404(task_id)
    
    if task.status != 'running':
        return jsonify({'error': 'Task is not running'}), 400
    
    # In a real implementation, this would signal the Celery task to stop
    task.status = 'stopped'
    task.end_time = datetime.utcnow()
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@training_bp.route('/tasks/<int:task_id>/metrics', methods=['GET'])
def get_training_metrics(task_id):
    """Get metrics for a training task"""
    task = TrainingTask.query.get_or_404(task_id)
    metrics = TrainingMetric.query.filter_by(task_id=task_id).order_by(TrainingMetric.epoch).all()
    
    return jsonify({
        'task': task.to_dict(),
        'metrics': [metric.to_dict() for metric in metrics]
    }), 200

@training_bp.route('/tasks/<int:task_id>/metrics', methods=['POST'])
def add_training_metric(task_id):
    """Add a new metric to a training task (used by training process)"""
    task = TrainingTask.query.get_or_404(task_id)
    data = request.get_json()
    
    metric = TrainingMetric(
        task_id=task_id,
        epoch=data.get('epoch'),
        loss=data.get('loss'),
        accuracy=data.get('accuracy'),
        validation_loss=data.get('validation_loss'),
        validation_accuracy=data.get('validation_accuracy'),
        learning_rate=data.get('learning_rate')
    )
    
    db.session.add(metric)
    
    # Update task progress
    task.current_epoch = data.get('epoch', task.current_epoch)
    task.loss = data.get('loss', task.loss)
    task.accuracy = data.get('accuracy', task.accuracy)
    task.validation_loss = data.get('validation_loss', task.validation_loss)
    task.validation_accuracy = data.get('validation_accuracy', task.validation_accuracy)
    
    if task.total_epochs:
        task.progress = (task.current_epoch / task.total_epochs) * 100
    
    db.session.commit()
    
    return jsonify(metric.to_dict()), 201

@training_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_training_task(task_id):
    """Delete a training task"""
    task = TrainingTask.query.get_or_404(task_id)
    
    if task.status == 'running':
        return jsonify({'error': 'Cannot delete a running task'}), 400
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Training task deleted successfully'}), 200
