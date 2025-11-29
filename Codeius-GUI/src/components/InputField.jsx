import React from 'react';
import '../App.css';

const InputField = () => {
  return (
    <div className="input-container">
      <input
        type="text"
        className="input-field"
        placeholder="Ask Codeius AI anything about your code..."
      />
    </div>
  );
};

export default InputField;