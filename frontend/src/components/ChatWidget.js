import React, { useState, useEffect, useRef } from 'react';
import { FaComments, FaTimes, FaPaperPlane, FaTrash } from 'react-icons/fa';
import { chatAPI, ChatSocket } from '../services/chatApi';
import '../styles/ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const chatSocketRef = useRef(null);

  // Scroll to bottom when messages update
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize WebSocket connection
  useEffect(() => {
    chatSocketRef.current = new ChatSocket();
    chatSocketRef.current.connect();

    // Listen for responses
    chatSocketRef.current.onMessage((data) => {
      setIsTyping(false);
      if (data.success && data.response) {
        const assistantMessage = {
          role: 'assistant',
          content: data.response.content,
          timestamp: new Date().toISOString(),
          type: data.response.type || 'text',
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else if (data.error) {
        const errorMessage = {
          role: 'assistant',
          content: `Error: ${data.error}`,
          timestamp: new Date().toISOString(),
          type: 'error',
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    });

    // Load chat history
    loadHistory();

    return () => {
      chatSocketRef.current?.disconnect();
    };
  }, []);

  const loadHistory = async () => {
    try {
      const response = await chatAPI.getHistory('default', 10);
      if (response.data.success) {
        const history = response.data.history.map(msg => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
          type: 'text',
        }));
        setMessages(history);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
      type: 'text',
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Send via WebSocket if connected, otherwise use REST API
    if (chatSocketRef.current?.socket?.connected) {
      chatSocketRef.current.sendMessage(inputMessage);
    } else {
      // Fallback to REST API
      try {
        setIsLoading(true);
        const response = await chatAPI.sendMessage(inputMessage);
        setIsTyping(false);
        if (response.data.success && response.data.response) {
          const assistantMessage = {
            role: 'assistant',
            content: response.data.response.content,
            timestamp: new Date().toISOString(),
            type: response.data.response.type || 'text',
          };
          setMessages(prev => [...prev, assistantMessage]);
        }
      } catch (error) {
        setIsTyping(false);
        const errorMessage = {
          role: 'assistant',
          content: 'Sorry, I encountered an error processing your request.',
          timestamp: new Date().toISOString(),
          type: 'error',
        };
        setMessages(prev => [...prev, errorMessage]);
        console.error('Failed to send message:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      try {
        await chatAPI.clearHistory();
        setMessages([]);
        const welcomeMessage = {
          role: 'assistant',
          content: 'Chat history cleared. How can I help you today?',
          timestamp: new Date().toISOString(),
          type: 'text',
        };
        setMessages([welcomeMessage]);
      } catch (error) {
        console.error('Failed to clear history:', error);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (message, index) => {
    const isUser = message.role === 'user';
    const isError = message.type === 'error';

    return (
      <div key={index} className={`message ${isUser ? 'user-message' : 'assistant-message'} ${isError ? 'error-message' : ''}`}>
        <div className="message-content">
          {message.content}
        </div>
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    );
  };

  const suggestedQueries = [
    'Show all models',
    'List datasets',
    'Show training tasks',
    'Platform statistics',
    'What formats are supported?',
  ];

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button className="chat-button" onClick={() => setIsOpen(true)}>
          <FaComments size={24} />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <div className="chat-title">
              <FaComments size={20} />
              <span>AI Assistant</span>
            </div>
            <div className="chat-actions">
              <button onClick={handleClearHistory} title="Clear History">
                <FaTrash size={16} />
              </button>
              <button onClick={() => setIsOpen(false)} title="Close">
                <FaTimes size={20} />
              </button>
            </div>
          </div>

          <div className="chat-body">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <h3>Welcome! 👋</h3>
                <p>I'm your AI assistant. I can help you with:</p>
                <ul>
                  <li>Managing models and datasets</li>
                  <li>Monitoring training tasks</li>
                  <li>Analyzing platform statistics</li>
                  <li>Answering questions about the platform</li>
                </ul>
                <div className="suggested-queries">
                  <p><strong>Try asking:</strong></p>
                  {suggestedQueries.map((query, idx) => (
                    <button
                      key={idx}
                      className="suggested-query"
                      onClick={() => {
                        setInputMessage(query);
                      }}
                    >
                      {query}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <>
                {messages.map((message, index) => renderMessage(message, index))}
                {isTyping && (
                  <div className="message assistant-message typing-indicator">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          <div className="chat-footer">
            <textarea
              className="chat-input"
              placeholder="Type your message..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              rows={1}
            />
            <button
              className="send-button"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
            >
              <FaPaperPlane size={18} />
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;
