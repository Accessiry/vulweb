import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..models import db, Dataset
from ..utils.file_utils import allowed_file
from ..services.dataset_service import analyze_dataset

dataset_bp = Blueprint('dataset', __name__, url_prefix='/api/datasets')

@dataset_bp.route('', methods=['GET'])
def get_datasets():
    """Get all datasets"""
    datasets = Dataset.query.order_by(Dataset.created_at.desc()).all()
    return jsonify([dataset.to_dict() for dataset in datasets]), 200

@dataset_bp.route('/<int:dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    """Get a specific dataset"""
    dataset = Dataset.query.get_or_404(dataset_id)
    return jsonify(dataset.to_dict()), 200

@dataset_bp.route('', methods=['POST'])
def create_dataset():
    """Create a new dataset"""
    data = request.form
    file = request.files.get('file')
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Dataset name is required'}), 400
    
    if not file:
        return jsonify({'error': 'Dataset file is required'}), 400
    
    # Check if dataset name already exists
    if Dataset.query.filter_by(name=data.get('name')).first():
        return jsonify({'error': 'Dataset name already exists'}), 400
    
    if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'error': 'Invalid file format'}), 400
    
    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'datasets', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Determine format
    file_format = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
    
    dataset = Dataset(
        name=data.get('name'),
        description=data.get('description'),
        file_path=file_path,
        format=file_format,
        size=file_size,
        preprocessing_status='pending'
    )
    
    db.session.add(dataset)
    db.session.commit()
    
    # Analyze dataset asynchronously
    try:
        stats = analyze_dataset(file_path, file_format)
        if stats:
            dataset.num_samples = stats.get('num_samples')
            dataset.num_vulnerable = stats.get('num_vulnerable')
            dataset.num_safe = stats.get('num_safe')
            dataset.preprocessing_status = 'completed'
            db.session.commit()
    except Exception as e:
        dataset.preprocessing_status = 'failed'
        db.session.commit()
        current_app.logger.error(f"Failed to analyze dataset: {str(e)}")
    
    return jsonify(dataset.to_dict()), 201

@dataset_bp.route('/<int:dataset_id>', methods=['PUT'])
def update_dataset(dataset_id):
    """Update a dataset"""
    dataset = Dataset.query.get_or_404(dataset_id)
    data = request.get_json()
    
    if 'name' in data:
        # Check if new name conflicts with another dataset
        existing = Dataset.query.filter_by(name=data['name']).first()
        if existing and existing.id != dataset_id:
            return jsonify({'error': 'Dataset name already exists'}), 400
        dataset.name = data['name']
    
    if 'description' in data:
        dataset.description = data['description']
    
    db.session.commit()
    
    return jsonify(dataset.to_dict()), 200

@dataset_bp.route('/<int:dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    """Delete a dataset"""
    dataset = Dataset.query.get_or_404(dataset_id)
    
    # Delete associated file if exists
    if dataset.file_path and os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    
    db.session.delete(dataset)
    db.session.commit()
    
    return jsonify({'message': 'Dataset deleted successfully'}), 200

@dataset_bp.route('/<int:dataset_id>/stats', methods=['GET'])
def get_dataset_stats(dataset_id):
    """Get dataset statistics"""
    dataset = Dataset.query.get_or_404(dataset_id)
    
    stats = {
        'id': dataset.id,
        'name': dataset.name,
        'num_samples': dataset.num_samples,
        'num_vulnerable': dataset.num_vulnerable,
        'num_safe': dataset.num_safe,
        'size': dataset.size,
        'format': dataset.format,
        'preprocessing_status': dataset.preprocessing_status
    }
    
    return jsonify(stats), 200
