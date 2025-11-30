import React, { useState, useRef, useEffect } from 'react';
import './App.css'
import Navbar from './components/Navbar/Navbar'
import InputField from './components/InputField/InputField'
import Sidebar from './components/Sidebar/Sidebar'
import ChatBubble from './components/ChatBubble/ChatBubble'
import HistoryModal from './components/HistoryModal/HistoryModal';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Codeius AI assistant. How can I help you today?",
      sender: 'ai',
      timestamp: new Date()
    }
  ]);

  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Function to open history modal
  const openHistoryModal = () => {
    setIsHistoryModalOpen(true);
  };

  // Function to close history modal
  const closeHistoryModal = () => {
    setIsHistoryModalOpen(false);
  };

  // Always auto-scroll to latest message for user messages, but track for AI responses
  const shouldAutoScroll = useRef(true);
  const latestUserMessageId = useRef(null);

  useEffect(() => {
    const container = chatContainerRef.current;
    if (container) {
      // Check if the latest message is from the user (they want to see their message)
      const latestMessage = messages[messages.length - 1];

      // If the latest message is from the user or it's the initial AI welcome message,
      // always scroll to bottom
      const isUserMessage = latestMessage?.sender === 'user';
      const isInitialMessage = messages.length === 1; // Welcome message

      if (isUserMessage || isInitialMessage) {
        // Always scroll to bottom for user messages and initial messages
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
          // Update the latest user message ID
          if (isUserMessage) {
            latestUserMessageId.current = latestMessage.id;
          }
        }, 10); // Small delay to ensure DOM has updated
      } else {
        // For AI messages, check if user was near bottom before
        const isNearBottom = container.scrollHeight - container.clientHeight - container.scrollTop < 100;

        if (isNearBottom) {
          // Scroll to bottom if user was already near bottom
          setTimeout(() => {
            messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
          }, 10);
        }
      }
    }
  }, [messages]);

  // Add scroll listener to detect when user scrolls up
  useEffect(() => {
    const container = chatContainerRef.current;

    const handleScroll = () => {
      if (container) {
        // Check if user has scrolled up significantly (more than 100px from bottom)
        const isNearBottom = container.scrollHeight - container.clientHeight - container.scrollTop < 100;
        shouldAutoScroll.current = isNearBottom;
      }
    };

    if (container) {
      container.addEventListener('scroll', handleScroll);
      // Cleanup listener on unmount
      return () => {
        container.removeEventListener('scroll', handleScroll);
      };
    }
  }, []);

  // Add keyboard navigation functionality
  useEffect(() => {
    const container = chatContainerRef.current;

    const handleKeyDown = (e) => {
      // Only respond to keys if the input field is not focused
      if (!document.activeElement.classList.contains('input-field')) {
        if (e.key === 'ArrowUp' && container) {
          e.preventDefault();
          // Scroll up by roughly 100px or to the top if near the top
          container.scrollTop = Math.max(0, container.scrollTop - 100);
        } else if (e.key === 'ArrowDown' && container) {
          e.preventDefault();
          // Scroll down by roughly 100px or to the bottom if near the bottom
          const maxScroll = container.scrollHeight - container.clientHeight;
          container.scrollTop = Math.min(maxScroll, container.scrollTop + 100);
        } else if (e.key === 'Home' && container) {
          e.preventDefault();
          // Scroll to top
          container.scrollTop = 0;
        } else if (e.key === 'End' && container) {
          e.preventDefault();
          // Scroll to bottom
          container.scrollTop = container.scrollHeight;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <div className="App">
      <Navbar onOpenHistory={openHistoryModal} />
      <Sidebar />
      {/* Chat bubbles appear on the background */}
      <div className="chat-bubbles-container" ref={chatContainerRef}>
        {messages.map((message) => (
          <ChatBubble
            key={message.id}
            text={message.text}
            sender={message.sender}
            timestamp={message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>
      {/* The background image remains visible as the background of the App div */}
      <InputField setMessages={setMessages} messages={messages} />
      {/* History modal */}
      <HistoryModal isOpen={isHistoryModalOpen} onClose={closeHistoryModal} />
    </div>
  )
}

export default App
