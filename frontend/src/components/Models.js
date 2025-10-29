import React, { useState, useEffect } from 'react';
import { modelsAPI } from '../services/api';
import { FaPlus, FaTrash } from 'react-icons/fa';
import '../styles/Models.css';

function Models() {
  const [models, setModels] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    version: '',
    model_type: 'vulnerability_detection',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await modelsAPI.getAll();
      setModels(response.data);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = new FormData();
      data.append('name', formData.name);
      data.append('description', formData.description);
      data.append('version', formData.version);
      data.append('model_type', formData.model_type);
      if (file) {
        data.append('file', file);
      }

      await modelsAPI.create(data);
      setShowForm(false);
      setFormData({ name: '', description: '', version: '', model_type: 'vulnerability_detection' });
      setFile(null);
      fetchModels();
    } catch (error) {
      console.error('Error creating model:', error);
      alert('Failed to create model');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this model?')) {
      try {
        await modelsAPI.delete(id);
        fetchModels();
      } catch (error) {
        console.error('Error deleting model:', error);
        alert('Failed to delete model');
      }
    }
  };

  return (
    <div className="models-container">
      <div className="header">
        <h1>Model Management</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <FaPlus /> Add Model
        </button>
      </div>

      {showForm && (
        <div className="form-container">
          <h2>Add New Model</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>Version</label>
              <input
                type="text"
                value={formData.version}
                onChange={(e) => setFormData({ ...formData, version: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Model Type</label>
              <select
                value={formData.model_type}
                onChange={(e) => setFormData({ ...formData, model_type: e.target.value })}
              >
                <option value="vulnerability_detection">Vulnerability Detection</option>
                <option value="fine_grained_location">Fine-Grained Location</option>
              </select>
            </div>
            <div className="form-group">
              <label>Model File</label>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                accept=".pkl,.pt,.pth,.h5"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Creating...' : 'Create Model'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="models-grid">
        {models.map((model) => (
          <div key={model.id} className="model-card">
            <div className="model-header">
              <h3>{model.name}</h3>
              <div className="model-actions">
                <button className="btn-icon" onClick={() => handleDelete(model.id)}>
                  <FaTrash />
                </button>
              </div>
            </div>
            <p className="model-description">{model.description || 'No description'}</p>
            <div className="model-info">
              <div className="info-item">
                <span className="label">Type:</span>
                <span className="value">{model.model_type || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="label">Version:</span>
                <span className="value">{model.version || 'N/A'}</span>
              </div>
              {model.accuracy && (
                <div className="info-item">
                  <span className="label">Accuracy:</span>
                  <span className="value">{(model.accuracy * 100).toFixed(2)}%</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {models.length === 0 && !showForm && (
        <div className="empty-state">
          <p>No models found. Create your first model to get started.</p>
        </div>
      )}
    </div>
  );
}

export default Models;
