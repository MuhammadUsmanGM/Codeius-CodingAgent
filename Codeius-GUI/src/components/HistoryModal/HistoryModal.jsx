import React, { useState, useEffect } from 'react';
import './HistoryModal.css';

const HistoryModal = ({ isOpen, onClose }) => {
  const [chatHistory, setChatHistory] = useState([]);

  // Load chat history from localStorage on component mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
      try {
        setChatHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Error parsing chat history:', e);
      }
    }
  }, []);

  // Clear chat history
  const clearHistory = () => {
    setChatHistory([]);
    localStorage.removeItem('chatHistory');
  };

  if (!isOpen) return null;

  return (
    <div className="history-modal-overlay" onClick={onClose}>
      <div className="history-modal" onClick={(e) => e.stopPropagation()}>
        <div className="history-modal-header">
          <h2>Chat History</h2>
        </div>
        
        <div className="history-modal-content">
          {chatHistory.length > 0 ? (
            <div className="history-list">
              {chatHistory.map((item, index) => (
                <div key={index} className="history-item">
                  <div className="history-conversation">
                    <div className="history-user-msg">
                      <strong>You:</strong> {item.userMsg}
                    </div>
                    <div className="history-ai-msg">
                      <strong>AI:</strong> {item.aiMsg}
                    </div>
                  </div>
                  <div className="history-timestamp">{item.timestamp}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="history-empty">
              <p>No chat history yet</p>
            </div>
          )}
        </div>
        
        <div className="history-modal-footer">
          <button className="clear-history-btn" onClick={clearHistory}>
            Clear History
          </button>
          <button className="close-history-btn" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default HistoryModal;