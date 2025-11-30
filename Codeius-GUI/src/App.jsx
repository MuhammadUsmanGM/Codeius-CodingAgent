import React, { useState, useRef, useEffect } from 'react';
import './App.css'
import Navbar from './components/Navbar/Navbar'
import InputField from './components/InputField/InputField'
import Sidebar from './components/Sidebar/Sidebar'
import ChatBubble from './components/ChatBubble/ChatBubble'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Codeius AI assistant. How can I help you today?",
      sender: 'ai',
      timestamp: new Date()
    }
  ]);

  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

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

  return (
    <div className="App">
      <Navbar />
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
    </div>
  )
}

export default App
