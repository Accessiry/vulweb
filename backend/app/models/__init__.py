from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Model(db.Model):
    """Model entity for storing ML model information"""
    __tablename__ = 'models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)
    version = db.Column(db.String(32))
    model_type = db.Column(db.String(64))  # e.g., 'vulnerability_detection', 'fine_grained_location'
    file_path = db.Column(db.String(256))
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    training_tasks = db.relationship('TrainingTask', backref='model', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'model_type': self.model_type,
            'file_path': self.file_path,
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Dataset(db.Model):
    """Dataset entity for storing dataset information"""
    __tablename__ = 'datasets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(256))
    format = db.Column(db.String(32))  # e.g., 'csv', 'json'
    size = db.Column(db.Integer)  # Size in bytes
    num_samples = db.Column(db.Integer)
    num_vulnerable = db.Column(db.Integer)
    num_safe = db.Column(db.Integer)
    preprocessing_status = db.Column(db.String(32), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    training_tasks = db.relationship('TrainingTask', backref='dataset', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'file_path': self.file_path,
            'format': self.format,
            'size': self.size,
            'num_samples': self.num_samples,
            'num_vulnerable': self.num_vulnerable,
            'num_safe': self.num_safe,
            'preprocessing_status': self.preprocessing_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TrainingTask(db.Model):
    """Training task entity for tracking model training"""
    __tablename__ = 'training_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    status = db.Column(db.String(32), default='pending')  # pending, running, completed, failed
    progress = db.Column(db.Float, default=0.0)  # 0-100
    current_epoch = db.Column(db.Integer, default=0)
    total_epochs = db.Column(db.Integer)
    loss = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    validation_loss = db.Column(db.Float)
    validation_accuracy = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    output_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    metrics = db.relationship('TrainingMetric', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model_id': self.model_id,
            'dataset_id': self.dataset_id,
            'status': self.status,
            'progress': self.progress,
            'current_epoch': self.current_epoch,
            'total_epochs': self.total_epochs,
            'loss': self.loss,
            'accuracy': self.accuracy,
            'validation_loss': self.validation_loss,
            'validation_accuracy': self.validation_accuracy,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'error_message': self.error_message,
            'output_path': self.output_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TrainingMetric(db.Model):
    """Training metrics for each epoch"""
    __tablename__ = 'training_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('training_tasks.id'))
    epoch = db.Column(db.Integer)
    loss = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    validation_loss = db.Column(db.Float)
    validation_accuracy = db.Column(db.Float)
    learning_rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'epoch': self.epoch,
            'loss': self.loss,
            'accuracy': self.accuracy,
            'validation_loss': self.validation_loss,
            'validation_accuracy': self.validation_accuracy,
            'learning_rate': self.learning_rate,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
