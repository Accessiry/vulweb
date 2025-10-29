import axios from 'axios';
import { io } from 'socket.io-client';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

// REST API for chat
export const chatAPI = {
  sendMessage: (message, sessionId = 'default') => 
    axios.post(`${API_BASE_URL}/chat/message`, { message, session_id: sessionId }),
  
  getHistory: (sessionId = 'default', limit = null) => {
    const params = limit ? { session_id: sessionId, limit } : { session_id: sessionId };
    return axios.get(`${API_BASE_URL}/chat/history`, { params });
  },
  
  clearHistory: (sessionId = 'default') =>
    axios.post(`${API_BASE_URL}/chat/clear`, { session_id: sessionId }),
};

// WebSocket connection
export class ChatSocket {
  constructor() {
    this.socket = null;
    this.sessionId = 'default';
  }

  connect(sessionId = 'default') {
    this.sessionId = sessionId;
    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
    });

    this.socket.on('connect', () => {
      console.log('Connected to chat server');
      this.socket.emit('join', { session_id: this.sessionId });
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from chat server');
    });

    this.socket.on('error', (error) => {
      console.error('Socket error:', error);
    });

    return this.socket;
  }

  sendMessage(message) {
    if (this.socket && this.socket.connected) {
      this.socket.emit('chat_message', {
        message,
        session_id: this.sessionId,
      });
    } else {
      console.error('Socket not connected');
    }
  }

  onMessage(callback) {
    if (this.socket) {
      this.socket.on('chat_response', callback);
    }
  }

  clearHistory() {
    if (this.socket && this.socket.connected) {
      this.socket.emit('clear_history', {
        session_id: this.sessionId,
      });
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.emit('leave', { session_id: this.sessionId });
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export default chatAPI;
