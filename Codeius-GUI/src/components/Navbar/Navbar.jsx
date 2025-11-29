import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-content">
        <div className="nav-logo">
          <img src="/favicon.png" alt="Codeius AI Logo" className="logo-icon" />
          <span className="logo-text">Codeius AI</span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;