# src/cli.py

import sys
import os
from coding_agent.agent import CodingAgent
from coding_agent.dashboard import Dashboard
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.box import HEAVY_HEAD
from rich import print as rprint
from rich.rule import Rule
import pyfiglet
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.shortcuts import CompleteStyle
load_dotenv()

console = Console()

def confirm_safe_execution(result):
    console.print("The agent wants to perform these actions:", style="bold yellow")
    console.print(result)
    try:
        ask = Prompt.ask("Proceed?", choices=["y", "N"], default="N").strip().lower()
        return ask == "y"
    except:
        # Fallback if prompt fails
        ask = input("Proceed? [y/N]: ").strip().lower()
        return ask == "y"

def display_mcp_servers(agent):
    """Display available MCP servers to the user"""
    # Get the MCP manager instance from the agent
    mcp_manager = agent.mcp_manager
    servers = mcp_manager.list_servers()
    
    if not servers:
        console.print("[yellow]No MCP servers available.[/yellow]")
        console.print("[dim]MCP servers provide access to various tools and services.[/dim]")
        return
    
    console.print("\n[bold blue]Available MCP Servers:[/bold blue]")
    for server in servers:
        status = "[green]ENABLED[/green]" if server.enabled else "[red]DISABLED[/red]"
        console.print(f"  [cyan]{server.name}[/cyan]: {server.description} - {status}")
        console.print(f"    Endpoint: {server.endpoint}")
        console.print(f"    Capabilities: {', '.join(server.capabilities)}")
    console.print("\n[bold]MCP servers provide additional tools like code execution and file access without external APIs.[/bold]\n")

def display_dashboard():
    """Display the real-time dashboard for code quality metrics"""
    dashboard = Dashboard()
    rich_table = dashboard.generate_rich_dashboard()
    console.print(rich_table)
    
    # Additional explanation
    console.print("\n[bold]Dashboard Legend:[/bold]")
    console.print("  ✅ Good - Metric is in healthy range")
    console.print("  ⚠️  Warning - Metric could be improved")
    console.print("  ❌ Poor - Metric needs attention\n")

def ocr_image(agent, image_path):
    """Process an image using OCR to extract text"""
    if not os.path.exists(image_path):
        console.print(f"[bold red]Error: Image file '{image_path}' does not exist.[/bold red]")
        return
    
    # Find the OCR provider
    ocr_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'ocr':
            ocr_provider = provider
            break
    
    if not ocr_provider:
        console.print("[bold red]Error: OCR server not available.[/bold red]")
        return
    
    # In a real implementation, we would send the image to the OCR server
    # For now, we'll just simulate the process
    console.print(f"[bold yellow]Processing image: {image_path}[/bold yellow]")
    console.print("[bold]This would send the image to the OCR server for text extraction...[/bold]")
    console.print("[dim]In a real implementation, the image would be sent to the OCR server and the text would be returned.[/dim]")

def refactor_code(agent, file_path):
    """Analyze and refactor code in the specified file"""
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error: File '{file_path}' does not exist.[/bold red]")
        return
    
    # Find the refactor provider
    refactor_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'refactor':
            refactor_provider = provider
            break
    
    if not refactor_provider:
        console.print("[bold red]Error: Refactor server not available.[/bold red]")
        return
    
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        return
    
    # In a real implementation, we would send the content to the refactor server
    # For now, we'll just simulate the process
    console.print(f"[bold yellow]Analyzing code in: {file_path}[/bold yellow]")
    console.print("[bold]This would send the code to the refactoring server for analysis...[/bold]")
    console.print("[dim]In a real implementation, the server would return issues and suggestions for refactoring.[/dim]")

def diff_files(agent, file1, file2):
    """Compare two files using the diff tool"""
    if not os.path.exists(file1):
        console.print(f"[bold red]Error: File '{file1}' does not exist.[/bold red]")
        return
    
    if not os.path.exists(file2):
        console.print(f"[bold red]Error: File '{file2}' does not exist.[/bold red]")
        return
    
    # Find the diff provider
    diff_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'diff':
            diff_provider = provider
            break
    
    if not diff_provider:
        console.print("[bold red]Error: Diff server not available.[/bold red]")
        return
    
    # In a real implementation, we would send the file paths to the diff server
    # For now, we'll just simulate the process
    console.print(f"[bold yellow]Comparing files: {file1} vs {file2}[/bold yellow]")
    console.print("[bold]This would send the files to the diff server for comparison...[/bold]")
    console.print("[dim]In a real implementation, the server would return the differences between the files.[/dim]")

def visualization_task(agent, metric_type):
    """Handle visualization tasks for plotting metrics"""
    # Find the visualization provider
    visualization_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'visualization':
            visualization_provider = provider
            break
    
    if not visualization_provider:
        console.print("[bold red]Error: Visualization server not available.[/bold red]")
        return
    
    console.print(f"[bold yellow]Creating plot for: {metric_type}[/bold yellow]")
    console.print("[bold]This would send the request to the visualization server...[/bold]")
    console.print("[dim]In a real implementation, the server would generate a plot and display it.[/dim]")

def package_inspect_task(agent, package_name):
    """Handle package inspection tasks"""
    # Find the package inspector provider
    inspector_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'package_inspector':
            inspector_provider = provider
            break
    
    if not inspector_provider:
        console.print("[bold red]Error: Package inspector server not available.[/bold red]")
        return
    
    console.print(f"[bold yellow]Inspecting package: {package_name}[/bold yellow]")
    console.print("[bold]This would send the request to the package inspector server...[/bold]")
    console.print("[dim]In a real implementation, the server would return detailed package information including dependencies, licenses, and vulnerabilities.[/dim]")

def self_document_task(agent, doc_type, *args):
    """Handle self-documenting tasks for updating documentation"""
    # Find the self-documenting provider
    doc_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'self_documenting':
            doc_provider = provider
            break
    
    if not doc_provider:
        console.print("[bold red]Error: Self-documenting server not available.[/bold red]")
        return
    
    if doc_type == 'authors':
        console.print(f"[bold yellow]Updating AUTHORS file with: {args}[/bold yellow]")
        console.print("[bold]This would send the request to the self-documenting server...[/bold]")
        console.print("[dim]In a real implementation, the server would update the AUTHORS file.[/dim]")
    
    elif doc_type == 'changelog':
        console.print(f"[bold yellow]Updating CHANGELOG with: {args}[/bold yellow]")
        console.print("[bold]This would send the request to the self-documenting server...[/bold]")
        console.print("[dim]In a real implementation, the server would update the CHANGELOG file.[/dim]")
    
    elif doc_type == 'readme':
        console.print(f"[bold yellow]Updating README section: {args}[/bold yellow]")
        console.print("[bold]This would send the request to the self-documenting server...[/bold]")
        console.print("[dim]In a real implementation, the server would update the README file.[/dim]")
    
    else:
        console.print(f"[bold red]Unknown documentation type: {doc_type}[/bold red]")

def automation_task(agent, task_type, *args):
    """Handle automation tasks like scaffolding, env management, and renaming"""
    # Find the automation provider
    automation_provider = None
    for provider in agent.providers:
        if hasattr(provider, 'server_name') and provider.server_name == 'automation':
            automation_provider = provider
            break
    
    if not automation_provider:
        console.print("[bold red]Error: Automation server not available.[/bold red]")
        return
    
    if task_type == 'scaffold':
        if len(args) < 1:
            console.print("[bold red]Please specify a project name. Usage: /scaffold [project_name] ([template])[/bold red]")
            return
        project_name = args[0]
        template = args[1] if len(args) > 1 else 'basic'
        console.print(f"[bold yellow]Creating project scaffold: {project_name} (template: {template})[/bold yellow]")
        console.print("[bold]This would send the request to the automation server...[/bold]")
        console.print("[dim]In a real implementation, the server would create the project structure.[/dim]")
    
    elif task_type == 'env':
        console.print(f"[bold yellow]Managing environment variables: {args}[/bold yellow]")
        console.print("[bold]This would send the request to the automation server...[/bold]")
        console.print("[dim]In a real implementation, the server would manage .env files.[/dim]")
    
    elif task_type == 'rename':
        if len(args) < 2:
            console.print("[bold red]Please specify old and new names. Usage: /rename [old_name] [new_name] ([file_path])[/bold red]")
            return
        old_name = args[0]
        new_name = args[1]
        file_path = args[2] if len(args) > 2 else 'current file'
        console.print(f"[bold yellow]Renaming variable: {old_name} → {new_name} in {file_path}[/bold yellow]")
        console.print("[bold]This would send the request to the automation server...[/bold]")
        console.print("[dim]In a real implementation, the server would rename variables in the file.[/dim]")
    
    else:
        console.print(f"[bold red]Unknown automation task: {task_type}[/bold red]")

def show_plugins(agent):
    """Display available plugins"""
    plugins = agent.plugin_manager.get_available_plugins()
    
    if not plugins:
        console.print("[yellow]No plugins available.[/yellow]")
        console.print("[dim]Create your own plugins by adding Python files to the plugins/ directory.[/dim]")
        return
    
    console.print("\n[bold blue]Available Plugins:[/bold blue]")
    for plugin_name, functions in plugins.items():
        console.print(f"  [cyan]{plugin_name}[/cyan]:")
        for func in functions:
            console.print(f"    - {func}")
    console.print("\n[bold]To create a plugin, add a Python file to the plugins/ directory.[/bold]\n")

def create_plugin(agent, name):
    """Create a new plugin skeleton"""
    try:
        plugin_path = agent.plugin_manager.create_plugin_skeleton(
            name=name,
            description=f"Custom plugin for {name}",
            author="User",
            version="1.0.0"
        )
        console.print(f"[bold green]Plugin '{name}' created successfully![/bold green]")
        console.print(f"Location: {plugin_path}")
        console.print("[dim]Edit this file to implement your plugin functionality.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error creating plugin: {e}[/bold red]")

def display_help():
    """Display help information with all available commands"""
    console.print("\n[bold blue]Available Commands:[/bold blue]")
    console.print("  [cyan]/models[/cyan] - List all available AI models")
    console.print("  [cyan]/mcp[/cyan] - List available MCP tools")
    console.print("  [cyan]/dashboard[/cyan] - Show real-time code quality dashboard")
    console.print("  [cyan]/ocr [image_path][/cyan] - Extract text from an image using OCR")
    console.print("  [cyan]/refactor [file_path][/cyan] - Analyze and refactor code in a file")
    console.print("  [cyan]/diff [file1] [file2][/cyan] - Compare two files or directories")
    console.print("  [cyan]/scaffold [name] [template][/cyan] - Generate project scaffolding")
    console.print("  [cyan]/env [action] [variables][/cyan] - Manage environment files")
    console.print("  [cyan]/rename [old] [new] [file][/cyan] - Batch rename variables")
    console.print("  [cyan]/plot [metric][/cyan] - Plot code metrics and data")
    console.print("  [cyan]/update_docs [type] [args][/cyan] - Update documentation files")
    console.print("  [cyan]/inspect [package][/cyan] - Inspect package information")
    console.print("  [cyan]/plugins[/cyan] - List available plugins")
    console.print("  [cyan]/create_plugin [name][/cyan] - Create a new plugin skeleton")
    console.print("  [cyan]/switch [model_key][/cyan] - Switch to a specific model")
    console.print("  [cyan]/help[/cyan] - Show this help message")
    console.print("  [cyan]/clear[/cyan] - Clear the conversation history")
    console.print("  [cyan]/exit[/cyan] - Exit the application\n")
    console.print("[bold blue]MCP Tools Available:[/bold blue]")
    console.print("  [cyan]code-runner[/cyan] - Execute Python code in sandboxed environment")
    console.print("  [cyan]filesystem[/cyan] - Access and manage files in workspace")
    console.print("  [cyan]duckduckgo[/cyan] - Perform web searches")
    console.print("  [cyan]code-search[/cyan] - Search for functions, classes, and TODOs in code")
    console.print("  [cyan]shell[/cyan] - Execute safe shell commands")
    console.print("  [cyan]testing[/cyan] - Run automated tests")
    console.print("  [cyan]doc-search[/cyan] - Search documentation files")
    console.print("  [cyan]database[/cyan] - Query local SQLite databases")
    console.print("  [cyan]ocr[/cyan] - Extract text from images")
    console.print("  [cyan]refactor[/cyan] - Analyze and refactor code")
    console.print("  [cyan]diff[/cyan] - Compare files and directories")
    console.print("  [cyan]automation[/cyan] - Automate repetitive coding tasks")
    console.print("  [cyan]visualization[/cyan] - Create plots and visualizations")
    console.print("  [cyan]self_documenting[/cyan] - Auto-update documentation")
    console.print("  [cyan]package_inspector[/cyan] - Inspect packages and dependencies\n")

def display_welcome_screen():
    """Display an enhanced welcome screen with project info and instructions"""
    # Display beautiful ASCII art for CODEIUS with improved font
    ascii_art = pyfiglet.figlet_format("CODEIUS", font="slant")
    console.print(f"[bold magenta]{ascii_art}[/bold magenta]")
    
    # Create a welcome table with project information
    welcome_table = Table(title="Welcome to Codeius AI Coding Agent", 
                         title_style="bold blue",
                         box=HEAVY_HEAD,
                         border_style="bright_blue",
                         expand=True)
    
    welcome_table.add_column("Feature", style="cyan", no_wrap=True)
    welcome_table.add_column("Description", style="white")
    
    welcome_table.add_row("📝 File Operations", "Read and write source files in the workspace")
    welcome_table.add_row("📦 Git Operations", "Perform git operations (stage, commit)")
    welcome_table.add_row("🌐 Web Search", "Perform real-time web searches via DuckDuckGo (no API key needed)")
    welcome_table.add_row("🤖 AI Integration", "Powered by multiple LLM providers (Groq, Google)")
    welcome_table.add_row("🛠️ MCP Servers", "Access additional tools via MCP protocol (code search, shell, testing, docs, databases)")
    welcome_table.add_row("📊 Dashboard", "Real-time code quality, test coverage, and build metrics")
    
    console.print(welcome_table)
    
    # Instructions panel
    instructions = (
        "[bold yellow]How to use:[/bold yellow]\n"
        "• Type your coding instructions in the input field\n"
        "• The agent will analyze your request and suggest actions\n"
        "• You'll be prompted to confirm any file changes or git operations\n"
        "• Type 'exit', 'quit', or 'bye' to exit the application\n"
    )
    console.print(Panel(instructions, title="[bold green]Instructions[/bold green]", expand=False))
    
    # Add a separator
    console.print(Rule(style="dim"))

def display_conversation_history(agent):
    """Display a summary of the conversation history"""
    if not agent.history:
        console.print("[italic dim]No conversation history yet.[/italic dim]")
        return
        
    console.print("\n[bold blue]Conversation History:[/bold blue]")
    for i, entry in enumerate(agent.history):
        role = entry["role"]
        content = entry["content"]
        if role == "user":
            console.print(f"[cyan]👤 You ({i+1}):[/cyan] {content[:100]}{'...' if len(content) > 100 else ''}")
        elif role == "assistant":
            content_preview = content[:100]
            # Remove any leading/trailing newlines or extra whitespace
            content_preview = content_preview.strip()
            console.print(f"[magenta]🤖 Agent ({i+1}):[/magenta] {content_preview}{'...' if len(content) > 100 else ''}")
    console.print()  # Add spacing

def display_models(agent):
    """Display available AI models to the user (excluding MCP tools)"""
    models = agent.get_available_models()
    current_model = agent.get_current_model_info()
    
    if not models:
        console.print("[yellow]No AI models available.[/yellow]")
        return
    
    console.print("\n[bold blue]Available AI Models:[/bold blue]")
    for key, model_info in models.items():
        if current_model and key == current_model['key']:
            # Highlight the currently active model
            console.print(f"  [green]→ {key}[/green]: {model_info['name']} ({model_info['provider']}) [Current]")
        else:
            console.print(f"  [cyan]{key}[/cyan]: {model_info['name']} ({model_info['provider']})")
    console.print("\n[bold]To switch models, use: /switch [model_key][/bold]\n")

def display_mcp_tools(agent):
    """Display available MCP tools to the user"""
    # Get all MCP tools from the agent
    mcp_tools = agent.get_available_mcp_tools()
    
    if not mcp_tools:
        console.print("[yellow]No MCP tools available.[/yellow]")
        console.print("[dim]MCP tools provide access to various utilities without requiring API keys.[/dim]")
        return
    
    console.print("\n[bold blue]Available MCP Tools:[/bold blue]")
    for key, tool_info in mcp_tools.items():
        console.print(f"  [cyan]{key}[/cyan]: {tool_info['name']} [MCP Tool]")
    console.print("\n[bold]MCP tools provide specialized functionality like code search, shell execution, etc.[/bold]\n")

class CustomCompleter(Completer):
    def __init__(self, agent):
        self.agent = agent

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith('/'):
            # Split the text to see if we're in a command or sub-command
            parts = text.split(' ', 1)
            command = parts[0].lower()
            
            if command == '/switch' or command.startswith('/switch'):
                # Show all models when user types /switch (with or without space)
                # The key is to check if we're after the /switch command
                if len(parts) > 1:
                    # User has started typing a model name after /switch, suggest matching models
                    typed_model = parts[1].lower()
                    models = self.agent.get_available_models()
                    current_model = self.agent.get_current_model_info()
                    for key, info in models.items():
                        if typed_model in key.lower() or typed_model in info['name'].lower():
                            # Highlight current model differently if possible
                            suffix = " [Current]" if (current_model and key == current_model['key']) else ""
                            yield Completion(key, start_position=-len(typed_model), 
                                           display=f"{key} [{info['name']}]",
                                           display_meta=f"{info['provider']}{suffix}")
                else:
                    # Show all models when user types /switch without any additional text
                    models = self.agent.get_available_models()
                    current_model = self.agent.get_current_model_info()
                    for key, info in models.items():
                        # Highlight current model in the suggestions
                        suffix = " [Current]" if (current_model and key == current_model['key']) else ""
                        yield Completion(key, 
                                       display=f"{key} [{info['name']}]",
                                       display_meta=f"{info['provider']}{suffix}")
            elif command in ['/help', '/clear', '/mcp', '/models', '/dashboard', '/ocr', '/refactor', '/diff', '/plugins', '/create_plugin', '/scaffold', '/env', '/rename', '/plot', '/update_docs', '/inspect', '/exit']:
                # Don't provide additional completions if these commands are fully typed
                pass
            else:
                # Provide command suggestions for commands that don't require parameters
                commands = ['/models', '/mcp', '/dashboard', '/ocr', '/refactor', '/diff', '/plugins', '/create_plugin', '/scaffold', '/env', '/rename', '/plot', '/update_docs', '/inspect', '/switch', '/help', '/clear', '/exit']
                for cmd in commands:
                    if cmd.startswith(text.lower()):
                        yield Completion(cmd, start_position=-len(text))

def main():
    display_welcome_screen()

    agent = CodingAgent()

    # Create a custom completer that handles both commands and model suggestions
    completer = CustomCompleter(agent)

    # Create a prompt session with styling and custom completion for a better input experience
    style = Style.from_dict({
        'prompt': 'bold cyan',
        'completion-menu': 'bg:#262626 #ffffff',
        'completion-menu.completion.current': 'bg:#4a4a4a #ffffff',
        'completion-menu.meta.completion': 'bg:#262626 #ffffff',
        'completion-menu.meta.completion.current': 'bg:#4a4a4a #ffffff',
    })
    
    session = PromptSession(
        completer=completer,
        style=style,
        complete_while_typing=True,
    )

    while True:
        try:
            # Styled prompt with more distinct visual indicator and auto-completion
            prompt_text = HTML('<style fg="cyan" bg="black">⌨️ Enter your query: </style> ')
            prompt = session.prompt(
                prompt_text,
                default='',
                complete_style=CompleteStyle.MULTI_COLUMN
            ).strip()

            if not prompt: continue
            
            # Handle special commands
            if prompt.startswith('/'):
                if prompt.lower() == '/models':
                    display_models(agent)
                    continue
                elif prompt.lower() == '/mcp':
                    display_mcp_tools(agent)
                    continue
                elif prompt.lower() == '/dashboard':
                    display_dashboard()
                    continue
                elif prompt.lower().startswith('/ocr '):
                    # Extract image path from the command
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        image_path = parts[1].strip()
                        ocr_image(agent, image_path)
                    else:
                        console.print("[bold red]Please specify an image path. Usage: /ocr [image_path][/bold red]")
                    continue
                elif prompt.lower().startswith('/refactor '):
                    # Extract file path from the command
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        file_path = parts[1].strip()
                        refactor_code(agent, file_path)
                    else:
                        console.print("[bold red]Please specify a file path. Usage: /refactor [file_path][/bold red]")
                    continue
                elif prompt.lower().startswith('/diff '):
                    # Extract file paths from the command
                    parts = prompt.split(' ', 2)  # Split into at most 3 parts: '/diff', 'file1', 'file2'
                    if len(parts) == 3:
                        file1, file2 = parts[1].strip(), parts[2].strip()
                        diff_files(agent, file1, file2)
                    else:
                        console.print("[bold red]Please specify two file paths. Usage: /diff [file1] [file2][/bold red]")
                    continue
                elif prompt.lower() == '/plugins':
                    show_plugins(agent)
                    continue
                elif prompt.lower().startswith('/create_plugin '):
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        plugin_name = parts[1].strip()
                        create_plugin(agent, plugin_name)
                    else:
                        console.print("[bold red]Please specify a plugin name. Usage: /create_plugin [name][/bold red]")
                    continue
                elif prompt.lower().startswith('/scaffold '):
                    parts = prompt.split(' ')
                    args = [part.strip() for part in parts[1:] if part.strip()]
                    automation_task(agent, 'scaffold', *args)
                    continue
                elif prompt.lower().startswith('/env '):
                    parts = prompt.split(' ')
                    args = [part.strip() for part in parts[1:] if part.strip()]
                    automation_task(agent, 'env', *args)
                    continue
                elif prompt.lower().startswith('/rename '):
                    parts = prompt.split(' ')
                    args = [part.strip() for part in parts[1:] if part.strip()]
                    automation_task(agent, 'rename', *args)
                    continue
                elif prompt.lower().startswith('/plot '):
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        metric_type = parts[1].strip()
                        visualization_task(agent, metric_type)
                    else:
                        console.print("[bold red]Please specify a metric type. Usage: /plot [metric_type][/bold red]")
                    continue
                elif prompt.lower().startswith('/update_docs '):
                    parts = prompt.split(' ', 2)
                    if len(parts) > 1:
                        doc_type = parts[1].strip()
                        doc_args = parts[2].split(' ') if len(parts) > 2 else []
                        self_document_task(agent, doc_type, *doc_args)
                    else:
                        console.print("[bold red]Please specify a documentation type. Usage: /update_docs [type] [args][/bold red]")
                    continue
                elif prompt.lower().startswith('/inspect '):
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        package_name = parts[1].strip()
                        package_inspect_task(agent, package_name)
                    else:
                        console.print("[bold red]Please specify a package name. Usage: /inspect [package_name][/bold red]")
                    continue
                elif prompt.lower().startswith('/switch '):
                    parts = prompt.split(' ', 1)
                    if len(parts) > 1:
                        model_key = parts[1].strip()
                        result = agent.switch_model(model_key)
                        console.print(Panel(result, title="[bold green]Model Switch[/bold green]", expand=False))
                        continue
                    else:
                        console.print("[bold red]Please specify a model. Use /models to see available models.[/bold red]")
                        continue
                elif prompt.lower() == '/help':
                    display_help()
                    continue
                elif prompt.lower() == '/clear':
                    agent.reset_history()
                    console.print("[bold green]✅ Conversation history cleared.[/bold green]")
                    continue
                elif prompt.lower() == '/exit':
                    # Allow user to exit using /exit command
                    # Display conversation history before exiting
                    console.print(Panel("[bold yellow]Conversation Summary[/bold yellow]", expand=False))
                    display_conversation_history(agent)
                    console.print("\n[bold green]👋 Thank you for using Codeius! Goodbye![/bold green]")
                    break
                else:
                    console.print(f"[bold red]Unknown command: {prompt}[/bold red]")
                    console.print("[bold yellow]Available commands: /models, /mcp, /dashboard, /switch [model_key], /help, /clear, /exit[/bold yellow]")
                    continue

            if prompt.lower() == "exit":
                # Display conversation history before exiting
                console.print(Panel("[bold yellow]Conversation Summary[/bold yellow]", expand=False))
                display_conversation_history(agent)
                console.print("\n[bold green]👋 Thank you for using Codeius! Goodbye![/bold green]")
                break
            result = agent.ask(prompt)
            if result.startswith("**Agent Plan:**"):  # Looks like JSON action plan is parsed
                if confirm_safe_execution(result):
                    console.print("\n[bold green]✅ Action(s) executed successfully.[/bold green]\n")
                else:
                    console.print("[bold red]❌ Action(s) cancelled.[/bold red]\n")
            else:
                # Enhanced agent response display 
                agent_panel = Panel(
                    result, 
                    title="[bold magenta]🤖 Codeius Agent[/bold magenta]", 
                    expand=False,
                    border_style="bright_magenta"
                )
                console.print(agent_panel)
                console.print()  # Add blank line for readability
                
            # Optionally show recent conversation history
            if len(agent.history) > 0 and len([h for h in agent.history if h["role"] == "user"]) % 3 == 0:
                show_history = Prompt.ask("\n[bold yellow]Show conversation history?[/bold yellow] [Y/n]", default="Y").strip().lower()
                if show_history in ("y", "yes", ""):
                    display_conversation_history(agent)
        except KeyboardInterrupt:
            console.print("\n[bold yellow]⚠️  Ctrl+C detected – exiting safely...[/bold yellow]")
            # Display conversation history before exiting
            console.print(Panel("[bold yellow]Conversation Summary[/bold yellow]", expand=False))
            display_conversation_history(agent)
            console.print("\n[bold green]👋 Thank you for using Codeius! Goodbye![/bold green]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")

if __name__ == "__main__":
    main()