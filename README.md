# README.md

# Codeius AI Coding Agent

Codeius is an AI-powered coding assistant that helps with various programming tasks through a command-line interface. It can read and write files, perform git operations, run tests, search code, execute shell commands, and conduct web searches to assist with coding tasks.

## Features

- **File Operations**: Read and write source files in your workspace
- **Git Operations**: Stage and commit files
- **Web Search**: Perform real-time web searches via DuckDuckGo MCP server (no API key required)
- **Multiple LLM Providers**: Uses both Groq and Google AI models with automatic failover
- **Model Switching**: Switch between available models using `/models` and `/switch` commands
- **Rich CLI Interface**: Beautiful, user-friendly command-line interface
- **Code Search & Navigation**: Find functions, classes, and TODOs in your project
- **Shell Commands**: Execute safe shell commands within the project
- **Automated Testing**: Run pytest tests directly from the agent
- **Documentation Search**: Find information in local documentation files
- **Database Access**: Query local SQLite databases safely
- **Real-time Dashboard**: Monitor code quality, test coverage, and build status
- **Visual Recognition/OCR**: Extract text from images using OCR
- **Code Refactoring & Quality**: Analyze code style, detect anti-patterns, and suggest refactorings
- **File/Directory Diff Tool**: Compare content of two files or directories for versioning and code reviews
- **Local Plugin System**: Extensible architecture allowing users to add custom tools by dropping in Python scripts
- **Script/Form Automation Tool**: Automate repetitive coding chores like scaffolding, environment management, and variable renaming
- **Data Visualization Tool**: Plot code metrics, test coverage, and database query results using matplotlib
- **Self-Documenting Agent**: Auto-update Markdown docs (AUTHORS, CHANGELOG, README) as code changes
- **Package Inspector**: Probe installed Python packages, license info, vulnerabilities, and dependencies offline
- **Snippet/Template Manager**: Store, retrieve, and insert boilerplate snippets for accelerating repetitive coding
- **Offline Web Scraping Tool**: Scrape static HTML files or local sites with BeautifulSoup, for documentation or data extraction tasks
- **Advanced Configuration/Settings Tool**: Interactive config/credentials manager for .env, YAML, or TOML settings—all changes local and secure
- **Scheduling/Task Automation Tool**: Local cron/task scheduler using schedule, letting the agent run commands, tests, or code checks automatically

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd coding-agent
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   # Additional dependencies for enhanced functionality:
   pip install flask pytest pillow pytesseract radon flake8 matplotlib packaging beautifulsoup4 pyyaml toml schedule
   ```

3. To use the enhanced functionality including task scheduling:
   You will need to run the following server scripts in separate terminals (only those you plan to use):
   - `python code_search_server.py` (port 9300)
   - `python shell_server.py` (port 9400)
   - `python testing_server.py` (port 9500)
   - `python doc_search_server.py` (port 9600)
   - `python db_server.py` (port 9700)
   - `python ocr_server.py` (port 9800)
   - `python refactor_server.py` (port 9900)
   - `python diff_server.py` (port 10000)
   - `python automation_server.py` (port 10100)
   - `python viz_server.py` (port 10200)
   - `python self_doc_server.py` (port 10300)
   - `python package_inspector_server.py` (port 10400)
   - `python snippet_manager_server.py` (port 10500)
   - `python web_scraper_server.py` (port 10600)
   - `python config_manager_server.py` (port 10700)
   - `python task_scheduler_server.py` (port 10800)

4. To add custom plugins:
   - Create Python files in the `plugins/` directory
   - Each file can contain multiple functions that will be auto-registered
   - Use `/plugins` to see available plugins
   - Use `/create_plugin [name]` to create a new plugin skeleton

5. To use automation tools:
   - Use `/scaffold [name] [template]` to generate project structures
   - Use `/env [action] [variables]` to manage environment files
   - Use `/rename [old] [new] [file]` to batch rename variables

6. To use visualization tools:
   - Use `/plot [metric_type]` to generate plots of code metrics, test coverage, or database results

7. To use self-documenting tools:
   - Use `/update_docs [type] [args]` to auto-update AUTHORS, CHANGELOG, README files

8. To use package inspection tools:
   - Use `/inspect [package_name]` to get detailed information about a package including dependencies, licenses, and vulnerabilities

9. To use snippet tools:
   - Use `/snippet [action] [args]` to manage code snippets with actions like 'get', 'add', 'list', and 'insert'

10. To use web scraping tools:
   - Use `/scrape [file_or_dir_or_url] [css_selector]` to scrape content from HTML files, directories, or URLs

11. To use configuration management tools:
   - Use `/config [action] [args]` to manage config files with actions like 'view', 'edit', and 'list'

12. To use scheduling automation tools:
   - Use `/schedule [task_type] [interval] [target]` to schedule tasks to run automatically (e.g., tests, scripts, commands)

## Configuration

Create a `.env` file in your project root with the following environment variables:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_MODEL=llama3-70b-8192  # Optional, defaults to llama3-70b-8192
GOOGLE_API_MODEL=gemini-1.5-flash  # Optional, defaults to gemini-1.5-flash
```

## Usage

Run the agent using:

```bash
coding-agent
```

### Available Commands

- `/models` - List available AI models
- `/mcp` - List available MCP servers
- `/dashboard` - Show real-time code quality dashboard
- `/switch [model_key]` - Switch to a specific model
- `/exit` - Exit the application
- `/help` - Show help information
- `/clear` - Clear the conversation history

### Example Usage

```
⌨️ Enter your query: Write a Python function to calculate factorial
🤖 Codeius Agent: [Response from the AI]
```

## Architecture

The agent follows a modular architecture:

- `agent.py` - Main agent logic and orchestration
- `cli.py` - Command-line interface
- `file_ops.py` - File system operations
- `git_ops.py` - Git operations
- `dashboard.py` - Code quality dashboard
- `history_manager.py` - Conversation history management
- `mcp_manager.py` - MCP server management
- `provider/` - LLM provider implementations
  - `groq.py` - Groq API integration
  - `google.py` - Google API integration
  - `mcp.py` - MCP server integration
  - `multiprovider.py` - Logic for switching between providers
- Server scripts:
  - `code_search_server.py` - Code search functionality
  - `shell_server.py` - Safe shell command execution
  - `testing_server.py` - Automated testing
  - `doc_search_server.py` - Documentation search
  - `db_server.py` - Database queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Specify your license here]