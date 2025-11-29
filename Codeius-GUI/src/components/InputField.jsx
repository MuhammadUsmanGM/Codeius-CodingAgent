import React, { useRef, useEffect } from 'react';

const InputField = () => {
  const textareaRef = useRef(null);

  const handleInput = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Reset height to auto to calculate the proper scrollHeight
    textarea.style.height = 'auto';
    
    // Calculate the new height based on content
    const maxHeight = 150; // Max height for 4 lines
    
    if (textarea.scrollHeight > maxHeight) {
      textarea.style.height = `${maxHeight}px`;
      textarea.style.overflowY = 'auto';
    } else {
      textarea.style.height = `${textarea.scrollHeight}px`;
      textarea.style.overflowY = 'hidden';
    }
  };

  useEffect(() => {
    // Set initial height on mount
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
    }
  }, []);

  return (
    <div className="input-container">
      <textarea
        ref={textareaRef}
        className="input-field"
        placeholder="Ask Codeius AI anything about your code..."
        onInput={handleInput}
        rows={1}
      />
    </div>
  );
};

export default InputField;