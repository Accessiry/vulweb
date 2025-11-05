# Models Directory

This directory stores trained machine learning models.

## Structure

Models uploaded through the web interface are stored in:
```
backend/uploads/models/
```

This directory is for reference and documentation purposes.

## Supported Formats

- `.pkl` - Pickle format (scikit-learn)
- `.pt` / `.pth` - PyTorch models
- `.h5` - Keras/TensorFlow models
- `.onnx` - ONNX format models

## Usage

Models are managed through the web interface:
1. Navigate to "Model Management"
2. Click "Upload Model"
3. Fill in model information
4. Select model file
5. Upload

## Model Information

Each model stores:
- Name and description
- Version number
- Model type (vulnerability_detection, fine_grained_location)
- Performance metrics (accuracy, precision, recall, f1_score)
- Training timestamps

## Best Practices

- Use descriptive model names
- Include version numbers
- Document model architecture
- Track training parameters
- Store model metadata
