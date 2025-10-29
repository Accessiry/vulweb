import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..models import db, Model
from ..utils.file_utils import allowed_file

model_bp = Blueprint('model', __name__, url_prefix='/api/models')

@model_bp.route('', methods=['GET'])
def get_models():
    """Get all models"""
    models = Model.query.order_by(Model.created_at.desc()).all()
    return jsonify([model.to_dict() for model in models]), 200

@model_bp.route('/<int:model_id>', methods=['GET'])
def get_model(model_id):
    """Get a specific model"""
    model = Model.query.get_or_404(model_id)
    return jsonify(model.to_dict()), 200

@model_bp.route('', methods=['POST'])
def create_model():
    """Create a new model"""
    data = request.form
    file = request.files.get('file')
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Model name is required'}), 400
    
    # Check if model name already exists
    if Model.query.filter_by(name=data.get('name')).first():
        return jsonify({'error': 'Model name already exists'}), 400
    
    file_path = None
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'models', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
    
    model = Model(
        name=data.get('name'),
        description=data.get('description'),
        version=data.get('version'),
        model_type=data.get('model_type', 'vulnerability_detection'),
        file_path=file_path,
        accuracy=float(data.get('accuracy', 0)) if data.get('accuracy') else None,
        precision=float(data.get('precision', 0)) if data.get('precision') else None,
        recall=float(data.get('recall', 0)) if data.get('recall') else None,
        f1_score=float(data.get('f1_score', 0)) if data.get('f1_score') else None
    )
    
    db.session.add(model)
    db.session.commit()
    
    return jsonify(model.to_dict()), 201

@model_bp.route('/<int:model_id>', methods=['PUT'])
def update_model(model_id):
    """Update a model"""
    model = Model.query.get_or_404(model_id)
    data = request.get_json()
    
    if 'name' in data:
        # Check if new name conflicts with another model
        existing = Model.query.filter_by(name=data['name']).first()
        if existing and existing.id != model_id:
            return jsonify({'error': 'Model name already exists'}), 400
        model.name = data['name']
    
    if 'description' in data:
        model.description = data['description']
    if 'version' in data:
        model.version = data['version']
    if 'model_type' in data:
        model.model_type = data['model_type']
    if 'accuracy' in data:
        model.accuracy = data['accuracy']
    if 'precision' in data:
        model.precision = data['precision']
    if 'recall' in data:
        model.recall = data['recall']
    if 'f1_score' in data:
        model.f1_score = data['f1_score']
    
    db.session.commit()
    
    return jsonify(model.to_dict()), 200

@model_bp.route('/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    """Delete a model"""
    model = Model.query.get_or_404(model_id)
    
    # Delete associated file if exists
    if model.file_path and os.path.exists(model.file_path):
        os.remove(model.file_path)
    
    db.session.delete(model)
    db.session.commit()
    
    return jsonify({'message': 'Model deleted successfully'}), 200
