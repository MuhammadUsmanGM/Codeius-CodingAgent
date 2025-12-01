import React from 'react';
import Settings from '../Settings/Settings';
import HistoryIcon from '../HistoryIcon/HistoryIcon';
import './Navbar.css';

const Navbar = ({ onOpenHistory, onModelChange, currentModel }) => {
  return (
    <nav className="navbar">
      <div className="nav-content">
        <div className="nav-spacer"></div>
        <div className="nav-logo">
          <img src="/favicon.png" alt="Codeius AI Logo" className="logo-icon" />
          <span className="logo-text">Codeius AI</span>
        </div>
        <div className="nav-controls"> {/* Combined controls section */}
          <HistoryIcon onOpenHistory={onOpenHistory} />
          <Settings onModelChange={onModelChange} currentModel={currentModel} />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;