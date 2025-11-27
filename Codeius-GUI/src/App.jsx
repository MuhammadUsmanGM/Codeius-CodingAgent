import { useState, useEffect, useRef } from 'react';
import './App.css';
import { AppShell, Burger, Group, Code, Text, Title, Stack, ScrollArea, NavLink, Accordion, ActionIcon, Flex } from '@mantine/core';
import { IconTerminal, IconAdjustments, IconApps, IconFileCode, IconSearch, IconShield, IconLayoutDashboard, IconPlayerPlay, IconTools, IconMenu2, IconX } from '@tabler/icons-react';

function App() {
  const [output, setOutput] = useState([{ id: 1, text: 'Welcome to Codeius Terminal!', type: 'system' }]);
  const [inputValue, setInputValue] = useState('');
  const [availableModels, setAvailableModels] = useState({});
  const [currentModel, setCurrentModel] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false); // Changed to false by default for AppShell
  const [commandHistory, setCommandHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const outputEndRef = useRef(null);

  const commandCategories = {
    "Basic Commands": [
      { name: '/help', description: 'Shows help information about available commands.' },
      { name: '/exit', description: 'Exits the agent application.' },
      { name: '/quit', description: 'Exits the agent application.' },
      { name: '/q', description: 'Exits the agent application.' },
    ],
    "Model Management Commands": [
      { name: '/models', description: 'Lists all available AI models and MCP tools.' },
      { name: '/switch [model_key]', description: 'Switches to a specific AI model by its key.' },
      { name: '/add_model', description: 'Adds a custom AI model from an OpenAI-compatible API endpoint.' },
    ],
    "MCP Server Commands": [
      { name: '/mcp', description: 'Lists available MCP servers and their status.' },
    ],
    "File and Project Management Commands": [
      { name: '/context', description: 'Shows current project context information.' },
      { name: '/set_project [path] [name]', description: 'Sets the current project context.' },
      { name: '/file_context [file_path]', description: 'Shows context information for a specific file.' },
      { name: '/autodetect', description: 'Auto-detects and sets project context.' },
    ],
    "Code Search and Navigation Commands": [
      { name: '/search [query]', description: 'Performs semantic search across the codebase.' },
      { name: '/find_function [name]', description: 'Finds a specific function by name.' },
      { name: '/find_class [name]', description: 'Finds a specific class by name.' },
    ],
    "Security Commands": [
      { name: '/security_scan', description: 'Runs a comprehensive security scan.' },
      { name: '/secrets_scan', description: 'Scans for secrets and sensitive information.' },
      { name: '/vuln_scan', description: 'Scans for code vulnerabilities.' },
      { name: '/policy_check', description: 'Checks for policy violations.' },
      { name: '/security_policy', description: 'Shows current security policy settings.' },
      { name: '/security_report', description: 'Generates a comprehensive security report.' },
      { name: '/set_policy [key] [value]', description: 'Updates security policy settings.' },
    ],
    "Interface and Display Commands": [
      { name: '/themes', description: 'Shows available visual themes.' },
      { name: '/dashboard', description: 'Shows real-time code quality dashboard.' },
      { name: '/cls', description: 'Clears the screen and refreshes the interface.' },
      { name: '/clear_screen', description: 'Clears the screen and refreshes the interface.' },
    ],
    "Mode Management Commands": [
      { name: '/toggle', description: 'Toggles between Interaction and Shell modes.' },
      { name: '/mode', description: 'Toggles between Interaction and Shell modes.' },
    ],
    "Development and Analysis Commands": [
      { name: '/shell [command]', description: 'Executes a direct shell command securely.' },
      { name: '/analyze [file_path]', description: 'Analyzes a code file for quality, security, and style issues.' },
      { name: '/clear', description: 'Clears the conversation history.' },
    ],
    "Additional Commands": [
      { name: '/keys', description: 'Shows mode switching options and keyboard shortcuts.' },
      { name: '/shortcuts', description: 'Shows mode switching options and keyboard shortcuts.' },
      { name: '/history', description: 'Shows the conversation history (if implemented).' },
    ],
  };

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
    if (cmd === 'clear' || cmd === '/cls' || cmd === '/clear_screen') {
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
    const newOutput = [...output, { id: Date.now() + 1, text: `$ ${cmd}`, type: 'command' }];

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
      const helpText = Object.entries(commandCategories).map(([category, cmds]) => {
        const cmdList = cmds.map(c => `  ${c.name.padEnd(25)} - ${c.description}`).join('\n');
        return `\n### ${category}\n${cmdList}`;
      }).join('\n');
      setOutput([...newOutput, { id: Date.now() + 1, text: `Available commands:\n${helpText}`, type: 'output' }]);
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
      const allCommands = Object.values(commandCategories).flat().map(cmd => cmd.name.split(' ')[0]);
      const matches = allCommands.filter(cmd => cmd.startsWith(inputValue));
      if (matches.length === 1) {
        setInputValue(matches[0]);
      }
    }
  };

  const runCommand = (cmd) => {
    setInputValue(cmd.startsWith('/') ? cmd : cmd.split(' ')[0]);
    setTimeout(() => {
      document.querySelector('.terminal-form')?.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }, 100);
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case "Basic Commands": return <IconTerminal size={18} />;
      case "Model Management Commands": return <IconAdjustments size={18} />;
      case "MCP Server Commands": return <IconApps size={18} />;
      case "File and Project Management Commands": return <IconFileCode size={18} />;
      case "Code Search and Navigation Commands": return <IconSearch size={18} />;
      case "Security Commands": return <IconShield size={18} />;
      case "Interface and Display Commands": return <IconLayoutDashboard size={18} />;
      case "Mode Management Commands": return <IconPlayerPlay size={18} />;
      case "Development and Analysis Commands": return <IconTools size={18} />;
      case "Additional Commands": return <IconMenu2 size={18} />;
      default: return <IconTerminal size={18} />;
    }
  };

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: 'sm',
        collapsed: { mobile: !sidebarOpen },
      }}
      padding="md"
    >
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger opened={sidebarOpen} onClick={() => setSidebarOpen((o) => !o)} hiddenFrom="sm" size="sm" />
          <Group justify="space-between" style={{ flex: 1 }}>
            <Title order={3} c="teal">
              Codeius AI
            </Title>
            <Flex align="center" gap="md">
              <Text size="sm">Current Model: <Code>{availableModels[currentModel]?.name || 'Loading...'}</Code></Text>
              <ActionIcon variant="default" size="lg">
                <IconX size={20} />
              </ActionIcon>
            </Flex>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <ScrollArea h="calc(100vh - 60px - 2rem)" mx="-md">
          <Accordion defaultValue="Basic Commands" variant="filled">
            {Object.entries(commandCategories).map(([category, cmds]) => (
              <Accordion.Item value={category} key={category}>
                <Accordion.Control icon={getCategoryIcon(category)}>
                  <Text fw={700}>{category}</Text>
                </Accordion.Control>
                <Accordion.Panel>
                  <Stack gap="xs">
                    {cmds.map((cmd, index) => (
                      <NavLink
                        key={index}
                        label={<Code>{cmd.name}</Code>}
                        description={cmd.description}
                        onClick={() => runCommand(cmd.name)}
                        variant="subtle"
                        active={inputValue.startsWith(cmd.name)}
                      />
                    ))}
                  </Stack>
                </Accordion.Panel>
              </Accordion.Item>
            ))}
          </Accordion>
        </ScrollArea>
      </AppShell.Navbar>

      <AppShell.Main>
        <div className="terminal-container">
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
      </AppShell.Main>
    </AppShell>
  );
}

export default App;
