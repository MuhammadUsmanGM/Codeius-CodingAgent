import { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [output, setOutput] = useState([{ id: 1, text: 'Welcome to Codeius Terminal!', type: 'system' }]);
  const [inputValue, setInputValue] = useState('');
  const [availableModels, setAvailableModels] = useState({});
  const [currentModel, setCurrentModel] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const outputEndRef = useRef(null);

  // Load available models on component mount
  useEffect(() => {
    fetchModels();
  }, []);

  // Scroll to bottom of output when it changes
  useEffect(() => {
    scrollToBottom();
  }, [output]);

  const scrollToBottom = () => {
    outputEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

  const fetchModels = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      const data = await response.json();
      setAvailableModels(data.models);

      // Set the first model as current if none is set
      if (Object.keys(data.models).length > 0 && !currentModel) {
        const firstModelKey = Object.keys(data.models)[0];
        setCurrentModel(firstModelKey);
      }
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const executeCommand = async (cmd) => {
    // Add user command to output
    const newOutput = [...output, { id: Date.now(), text: `$ ${cmd}`, type: 'command' }];
    setOutput(newOutput);

    // Add to command history
    setCommandHistory(prev => [...prev, cmd]);
    setHistoryIndex(-1);

    // Process the command
    if (cmd === 'clear') {
      setOutput([]);
    } else if (cmd.startsWith('/')) {
      // Handle Codeius-specific commands
      await processCodeiusCommand(cmd);
    } else {
      // Treat as a regular query to the AI
      await askAI(cmd);
    }
  };

  const processCodeiusCommand = async (cmd) => {
    // Add to output
    const newOutput = [...output, { id: Date.now(), text: `$ ${cmd}`, type: 'command' }];

    if (cmd === '/models') {
      const modelsList = Object.values(availableModels).map(model =>
        `- ${model.name} (${model.provider})`
      ).join('\n');
      setOutput([...newOutput, { id: Date.now() + 1, text: modelsList || 'No models available', type: 'output' }]);
    } else if (cmd === '/mcp') {
      setOutput([...newOutput, { id: Date.now() + 1, text: 'No MCP tools currently available', type: 'output' }]);
    } else if (cmd === '/dashboard') {
      setOutput([...newOutput, { id: Date.now() + 1, text: 'Dashboard not implemented yet in web interface', type: 'output' }]);
    } else if (cmd === '/themes') {
      setOutput([...newOutput, { id: Date.now() + 1, text: 'Available themes: default, dark, solarized, terminal', type: 'output' }]);
    } else if (cmd.startsWith('/switch')) {
      const modelKey = cmd.split(' ')[1];
      if (modelKey && availableModels[modelKey]) {
        try {
          const response = await fetch(`${API_BASE_URL}/switch_model`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_key: modelKey }),
          });
          const data = await response.json();
          setOutput([...newOutput, { id: Date.now() + 1, text: data.result, type: 'output' }]);
          setCurrentModel(modelKey);
        } catch (error) {
          setOutput([...newOutput, { id: Date.now() + 1, text: `Error: ${error.message}`, type: 'error' }]);
        }
      } else {
        setOutput([...newOutput, { id: Date.now() + 1, text: 'Usage: /switch [model_key]', type: 'error' }]);
      }
    } else if (cmd === '/help') {
      const helpText = `
Available commands:
/help          - Show this help message
/models        - List available AI models
/switch <key>  - Switch to a specific model
/mcp           - List available MCP tools
/dashboard     - Show dashboard (not implemented in web)
/themes        - Show available themes
/clear         - Clear the terminal
      `.trim();
      setOutput([...newOutput, { id: Date.now() + 1, text: helpText, type: 'output' }]);
    } else if (cmd === '/test') {
      setOutput([...newOutput, { id: Date.now() + 1, text: 'Test successful!', type: 'output' }]);
    } else {
      setOutput([...newOutput, { id: Date.now() + 1, text: `Unknown command: ${cmd}. Type /help for available commands.`, type: 'error' }]);
    }
  };

  const askAI = async (prompt) => {
    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      if (response.ok) {
        setOutput(prev => [...prev, { id: Date.now() + 1, text: data.response, type: 'ai-response' }]);
      } else {
        setOutput(prev => [...prev, { id: Date.now() + 1, text: `Error: ${data.error}`, type: 'error' }]);
      }
    } catch (error) {
      setOutput(prev => [...prev, { id: Date.now() + 1, text: `Network error: ${error.message}`, type: 'error' }]);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    executeCommand(inputValue.trim());
    setInputValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (commandHistory.length > 0) {
        const newIndex = historyIndex < commandHistory.length - 1 ? historyIndex + 1 : commandHistory.length - 1;
        setHistoryIndex(newIndex);
        setInputValue(commandHistory[commandHistory.length - 1 - newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInputValue(commandHistory[commandHistory.length - 1 - newIndex]);
      } else if (historyIndex === 0) {
        setHistoryIndex(-1);
        setInputValue('');
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // Basic command completion
      const commands = ['/help', '/models', '/switch', '/mcp', '/dashboard', '/themes', '/clear'];
      const matches = commands.filter(cmd => cmd.startsWith(inputValue));
      if (matches.length === 1) {
        setInputValue(matches[0]);
      }
    }
  };

  // Define available commands for the sidebar
  const commands = [
    { name: '/help', description: 'Show available commands' },
    { name: '/models', description: 'List AI models' },
    { name: '/switch [key]', description: 'Switch AI model' },
    { name: '/mcp', description: 'List MCP tools' },
    { name: '/dashboard', description: 'Show dashboard' },
    { name: '/themes', description: 'Show themes' },
    { name: '/clear', description: 'Clear terminal' },
    { name: '/shell [cmd]', description: 'Execute shell command' },
    { name: '/ocr [path]', description: 'OCR from image' },
    { name: '/refactor [path]', description: 'Refactor code' },
    { name: '/diff [file1] [file2]', description: 'Compare files' },
    { name: '/plot [metric]', description: 'Plot metrics' },
    { name: '/context', description: 'Show project context' },
    { name: '/search [query]', description: 'Search codebase' },
    { name: '/security_scan', description: 'Run security scan' },
    { name: '/plugins', description: 'List plugins' },
    { name: '/analyze', description: 'Analyze project' },
    { name: '/test', description: 'Run tests' },
    { name: '/exit', description: 'Exit terminal' },
  ];

  const runCommand = (cmd) => {
    setInputValue(cmd.startsWith('/') ? cmd : cmd.split(' ')[0]);
    setTimeout(() => {
      document.querySelector('.terminal-form')?.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }, 100);
  };

  return (
    <div className="app">
      {/* Sidebar with commands */}
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>🤖 Codeius</h2>
          <button
            className="menu-btn-small"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? '✕' : '☰'}
          </button>
        </div>

        <div className="commands-list">
          <h3>Commands</h3>
          {commands.map((cmd, index) => (
            <div
              key={index}
              className="command-item"
              onClick={() => runCommand(cmd.name)}
              title={cmd.description}
            >
              <span className="command-name">{cmd.name}</span>
              <span className="command-desc">{cmd.description}</span>
            </div>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="current-model">
            <span>Model: {availableModels[currentModel]?.name || 'Loading...'}</span>
          </div>
          <div className="model-select-container">
            <select
              value={currentModel}
              onChange={(e) => runCommand(`/switch ${e.target.value}`)}
              className="model-select-sidebar"
            >
              {Object.entries(availableModels).map(([key, model]) => (
                <option key={key} value={key}>
                  {model.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main terminal content */}
      <div className="terminal-container">
        <header className="terminal-header">
          <button
            className="menu-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>
          <div className="terminal-title">Codeius Terminal</div>
          <div className="terminal-controls">
            <button className="control-btn">−</button>
            <button className="control-btn">□</button>
            <button className="control-btn">×</button>
          </div>
        </header>

        <div className="terminal-output">
          {output.map((item) => (
            <div key={item.id} className={`terminal-line terminal-${item.type}`}>
              {item.type === 'command' ? '$ ' : ''}
              {item.text.split('\n').map((line, i) => (
                <div key={i}>{line}</div>
              ))}
            </div>
          ))}
          <div ref={outputEndRef} />
        </div>

        <form onSubmit={handleFormSubmit} className="terminal-form">
          <div className="prompt">$</div>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or ask a question..."
            className="terminal-input"
            autoFocus
          />
        </form>
      </div>

      {/* Overlay for mobile sidebar */}
      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}

export default App;
