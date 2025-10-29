import React, { useState, useEffect } from 'react';
import { datasetsAPI } from '../services/api';
import { FaPlus, FaTrash } from 'react-icons/fa';
import '../styles/Datasets.css';

function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await datasetsAPI.getAll();
      setDatasets(response.data);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file');
      return;
    }

    setLoading(true);

    try {
      const data = new FormData();
      data.append('name', formData.name);
      data.append('description', formData.description);
      data.append('file', file);

      await datasetsAPI.create(data);
      setShowForm(false);
      setFormData({ name: '', description: '' });
      setFile(null);
      fetchDatasets();
    } catch (error) {
      console.error('Error creating dataset:', error);
      alert('Failed to create dataset');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await datasetsAPI.delete(id);
        fetchDatasets();
      } catch (error) {
        console.error('Error deleting dataset:', error);
        alert('Failed to delete dataset');
      }
    }
  };

  const formatBytes = (bytes) => {
    if (!bytes) return 'N/A';
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(2)} MB`;
  };

  return (
    <div className="datasets-container">
      <div className="header">
        <h1>Dataset Management</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <FaPlus /> Add Dataset
        </button>
      </div>

      {showForm && (
        <div className="form-container">
          <h2>Add New Dataset</h2>
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
              <label>Dataset File *</label>
              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                accept=".json,.csv,.txt,.zip"
                required
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Uploading...' : 'Upload Dataset'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="datasets-grid">
        {datasets.map((dataset) => (
          <div key={dataset.id} className="dataset-card">
            <div className="dataset-header">
              <h3>{dataset.name}</h3>
              <div className="dataset-actions">
                <button className="btn-icon" onClick={() => handleDelete(dataset.id)}>
                  <FaTrash />
                </button>
              </div>
            </div>
            <p className="dataset-description">{dataset.description || 'No description'}</p>
            <div className="dataset-info">
              <div className="info-item">
                <span className="label">Format:</span>
                <span className="value">{dataset.format || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="label">Size:</span>
                <span className="value">{formatBytes(dataset.size)}</span>
              </div>
              <div className="info-item">
                <span className="label">Samples:</span>
                <span className="value">{dataset.num_samples || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="label">Status:</span>
                <span className={`status ${dataset.preprocessing_status}`}>
                  {dataset.preprocessing_status}
                </span>
              </div>
            </div>
            {dataset.num_vulnerable !== null && (
              <div className="dataset-stats">
                <div className="stat">
                  <span className="stat-label">Vulnerable:</span>
                  <span className="stat-value vulnerable">{dataset.num_vulnerable}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Safe:</span>
                  <span className="stat-value safe">{dataset.num_safe}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {datasets.length === 0 && !showForm && (
        <div className="empty-state">
          <p>No datasets found. Upload your first dataset to get started.</p>
        </div>
      )}
    </div>
  );
}

export default Datasets;
