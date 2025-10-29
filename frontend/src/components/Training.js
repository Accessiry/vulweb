import React, { useState, useEffect } from 'react';
import { trainingAPI, modelsAPI, datasetsAPI } from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FaPlay, FaStop, FaTrash } from 'react-icons/fa';
import '../styles/Training.css';

function Training() {
  const [tasks, setTasks] = useState([]);
  const [models, setModels] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    model_id: '',
    dataset_id: '',
    epochs: 10,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTasks();
    fetchModels();
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (selectedTask) {
      fetchMetrics(selectedTask.id);
      const interval = setInterval(() => {
        fetchMetrics(selectedTask.id);
        fetchTasks();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [selectedTask]);

  const fetchTasks = async () => {
    try {
      const response = await trainingAPI.getTasks();
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const fetchModels = async () => {
    try {
      const response = await modelsAPI.getAll();
      setModels(response.data);
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const fetchDatasets = async () => {
    try {
      const response = await datasetsAPI.getAll();
      setDatasets(response.data);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const fetchMetrics = async (taskId) => {
    try {
      const response = await trainingAPI.getMetrics(taskId);
      setMetrics(response.data.metrics || []);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await trainingAPI.createTask({
        name: formData.name,
        model_id: parseInt(formData.model_id),
        dataset_id: parseInt(formData.dataset_id),
        epochs: parseInt(formData.epochs),
      });
      setShowForm(false);
      setFormData({ name: '', model_id: '', dataset_id: '', epochs: 10 });
      fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      alert('Failed to create training task');
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async (taskId) => {
    try {
      await trainingAPI.stopTask(taskId);
      fetchTasks();
    } catch (error) {
      console.error('Error stopping task:', error);
      alert('Failed to stop task');
    }
  };

  const handleDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await trainingAPI.deleteTask(taskId);
        if (selectedTask?.id === taskId) {
          setSelectedTask(null);
          setMetrics([]);
        }
        fetchTasks();
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task');
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'green';
      case 'running':
        return 'blue';
      case 'failed':
        return 'red';
      default:
        return 'gray';
    }
  };

  return (
    <div className="training-container">
      <div className="header">
        <h1>Training & Validation</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <FaPlay /> Start Training
        </button>
      </div>

      {showForm && (
        <div className="form-container">
          <h2>Create Training Task</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Task Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Model *</label>
              <select
                value={formData.model_id}
                onChange={(e) => setFormData({ ...formData, model_id: e.target.value })}
                required
              >
                <option value="">Select a model</option>
                {models.map((model) => (
                  <option key={model.id} value={model.id}>
                    {model.name} ({model.version})
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Dataset *</label>
              <select
                value={formData.dataset_id}
                onChange={(e) => setFormData({ ...formData, dataset_id: e.target.value })}
                required
              >
                <option value="">Select a dataset</option>
                {datasets.map((dataset) => (
                  <option key={dataset.id} value={dataset.id}>
                    {dataset.name} ({dataset.num_samples} samples)
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Epochs</label>
              <input
                type="number"
                value={formData.epochs}
                onChange={(e) => setFormData({ ...formData, epochs: e.target.value })}
                min="1"
                max="1000"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Starting...' : 'Start Training'}
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="training-layout">
        <div className="tasks-list">
          <h2>Training Tasks</h2>
          {tasks.map((task) => (
            <div
              key={task.id}
              className={`task-card ${selectedTask?.id === task.id ? 'selected' : ''}`}
              onClick={() => setSelectedTask(task)}
            >
              <div className="task-header">
                <h3>{task.name}</h3>
                <span className={`status-badge ${task.status}`} style={{ backgroundColor: getStatusColor(task.status) }}>
                  {task.status}
                </span>
              </div>
              <div className="task-info">
                <div className="info-row">
                  <span>Progress:</span>
                  <span>{task.progress?.toFixed(1)}%</span>
                </div>
                <div className="info-row">
                  <span>Epoch:</span>
                  <span>{task.current_epoch}/{task.total_epochs}</span>
                </div>
                {task.accuracy && (
                  <div className="info-row">
                    <span>Accuracy:</span>
                    <span>{(task.accuracy * 100).toFixed(2)}%</span>
                  </div>
                )}
              </div>
              <div className="task-actions">
                {task.status === 'running' && (
                  <button className="btn-icon" onClick={(e) => { e.stopPropagation(); handleStop(task.id); }}>
                    <FaStop />
                  </button>
                )}
                {task.status !== 'running' && (
                  <button className="btn-icon" onClick={(e) => { e.stopPropagation(); handleDelete(task.id); }}>
                    <FaTrash />
                  </button>
                )}
              </div>
            </div>
          ))}
          {tasks.length === 0 && (
            <div className="empty-state">
              <p>No training tasks yet.</p>
            </div>
          )}
        </div>

        <div className="metrics-panel">
          {selectedTask ? (
            <>
              <h2>Training Metrics - {selectedTask.name}</h2>
              <div className="metrics-summary">
                <div className="metric-card">
                  <div className="metric-label">Loss</div>
                  <div className="metric-value">{selectedTask.loss?.toFixed(4) || 'N/A'}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Accuracy</div>
                  <div className="metric-value">{selectedTask.accuracy ? (selectedTask.accuracy * 100).toFixed(2) + '%' : 'N/A'}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Val Loss</div>
                  <div className="metric-value">{selectedTask.validation_loss?.toFixed(4) || 'N/A'}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Val Accuracy</div>
                  <div className="metric-value">{selectedTask.validation_accuracy ? (selectedTask.validation_accuracy * 100).toFixed(2) + '%' : 'N/A'}</div>
                </div>
              </div>

              {metrics.length > 0 && (
                <div className="charts">
                  <div className="chart-container">
                    <h3>Loss Over Time</h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <LineChart data={metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="epoch" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="loss" stroke="#8884d8" name="Training Loss" />
                        <Line type="monotone" dataKey="validation_loss" stroke="#82ca9d" name="Validation Loss" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="chart-container">
                    <h3>Accuracy Over Time</h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <LineChart data={metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="epoch" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="accuracy" stroke="#8884d8" name="Training Accuracy" />
                        <Line type="monotone" dataKey="validation_accuracy" stroke="#82ca9d" name="Validation Accuracy" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <p>Select a task to view metrics</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Training;
