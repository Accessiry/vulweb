import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Models from './components/Models';
import Datasets from './components/Datasets';
import Training from './components/Training';
import ChatWidget from './components/ChatWidget';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <h1>VulWeb ML Platform</h1>
          </div>
          <div className="nav-links">
            <Link to="/" className="nav-link">Models</Link>
            <Link to="/datasets" className="nav-link">Datasets</Link>
            <Link to="/training" className="nav-link">Training</Link>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<Models />} />
            <Route path="/datasets" element={<Datasets />} />
            <Route path="/training" element={<Training />} />
          </Routes>
        </div>

        {/* AI Chat Widget */}
        <ChatWidget />
      </div>
    </Router>
  );
}

export default App;
