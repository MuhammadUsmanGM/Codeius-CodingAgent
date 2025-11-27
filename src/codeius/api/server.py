# api/server.py

import os
import socket
from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from codeius.core.agent import CodingAgent

# Construct the absolute path to the dist folder directly
import os
# The relative path from this file to the dist folder is: ../../Codeius-GUI/dist
current_file_dir = os.path.dirname(os.path.abspath(__file__))  # src/codeius/api/
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file_dir)))  # project root
dist_path = os.path.join(project_root_dir, 'Codeius-GUI', 'dist')

# Verify the path exists before creating Flask app
print(f"Looking for dist folder at: {dist_path}")
print(f"Dist folder exists: {os.path.exists(dist_path)}")

app = Flask(__name__,
           static_folder=dist_path,
           template_folder=dist_path)

# Enable CORS for all routes and allow development origin
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:*", "http://127.0.0.1:*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# For SocketIO, we'll allow all origins for development but can be restricted in production
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:*", "http://127.0.0.1:*"])
agent = CodingAgent()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Check if static folder exists (the React build)
    if app.static_folder and os.path.exists(app.static_folder):
        # If path is not empty, try to serve the specific file
        if path:
            static_path = os.path.join(app.static_folder, path)
            if os.path.exists(static_path):
                return send_from_directory(app.static_folder, path)
            else:
                # If file doesn't exist, serve index.html for client-side routing
                return send_from_directory(app.static_folder, 'index.html')
        else:
            # If root path, serve index.html
            return send_from_directory(app.static_folder, 'index.html')

    # If no static folder exists, return an error (this shouldn't happen if build was done)
    return "React application not built. Run 'npm run build' in Codeius-GUI directory.", 500

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        socketio.emit('agent_thinking', {'thinking': True})
        response = agent.ask(prompt)
        socketio.emit('agent_thinking', {'thinking': False})

        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in /api/ask endpoint: {str(e)}")
        return jsonify({'error': 'Failed to process request', 'details': str(e)}), 500

@app.route('/api/history')
def history():
    try:
        return jsonify({'history': agent.conversation_manager.get_conversation_context()})
    except Exception as e:
        print(f"Error in /api/history endpoint: {str(e)}")
        return jsonify({'error': 'Failed to get history', 'details': str(e)}), 500

@app.route('/api/models')
def models():
    """Get available models"""
    try:
        models = agent.get_available_models()
        # Convert model objects to a list of dictionaries with 'name' and 'key'
        serializable_models = [{"name": model.name, "key": model.key} for model in models]
        return jsonify({'models': serializable_models})
    except Exception as e:
        print(f"Error in /api/models endpoint: {str(e)}")
        return jsonify({'error': 'Failed to get models', 'details': str(e)}), 500

@app.route('/api/switch_model', methods=['POST'])
def switch_model():
    """Switch to a specific model"""
    try:
        data = request.get_json()
        model_key = data.get('model_key')
        if not model_key:
            return jsonify({'error': 'No model key provided'}), 400

        result = agent.switch_model(model_key)
        return jsonify({'result': result})
    except Exception as e:
        print(f"Error in /api/switch_model endpoint: {str(e)}")
        return jsonify({'error': 'Failed to switch model', 'details': str(e)}), 500

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        agent.reset_history()
        return jsonify({'result': 'History cleared'})
    except Exception as e:
        print(f"Error in /api/clear_history endpoint: {str(e)}")
        return jsonify({'error': 'Failed to clear history', 'details': str(e)}), 500

def find_free_port(start_port=8080):
    """Find an available port to run the server on, starting with a default port."""
    # Try the default port first
    default_port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', default_port))
                s.listen(1)
                port = default_port
                s.close()  # Close the socket after finding a free port
                return port
            except OSError:
                # Port is in use, try the next one
                default_port += 1
                if default_port > 65535:  # Port range limit
                    # If we've exhausted the range, go back to auto-assign
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('', 0))
                        s.listen(1)
                        port = s.getsockname()[1]
                    return port

def get_network_ip():
    """Get the machine's network IP address"""
    import socket
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def run_gui():
    """Starts the Flask server on an available port."""
    import threading
    import webbrowser
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    # Create a rich console for better formatting
    console = Console()

    port = find_free_port(8080)  # Default to port 8080, then try consecutive ports
    local_url = f"http://localhost:{port}"
    network_url = f"http://{get_network_ip()}:{port}"

    # Print starting message
    console.print("Starting Codeius Web...", style="bold blue")

    # Create a table for URLs
    table = Table(title="[bold green]Welcome to Codeius Web[/bold green]",
                 title_justify="center",
                 show_header=True,
                 header_style="bold magenta",
                 border_style="blue",
                 title_style="bold green")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("URL", style="green")

    table.add_row("Local", local_url)
    table.add_row("Network", network_url)

    console.print(table)
    console.print("[bold yellow]Press 'o' to open in browser (one time only), or Ctrl+C to exit[/bold yellow]")

    # Define variables to control the key listener
    global should_open_browser, browser_opened
    should_open_browser = False
    browser_opened = False  # Flag to prevent multiple openings

    def check_keypress():
        global should_open_browser, browser_opened
        try:
            import keyboard
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name.lower() == 'o' and not browser_opened:
                        should_open_browser = True
                        browser_opened = True
                        webbrowser.open(local_url)
                        console.print("\n[bold green]✓ Browser opened successfully![/bold green]")
                        console.print("[bold yellow]Browser already opened. Press Ctrl+C to exit.[/bold yellow]")
                    elif event.name.lower() == 'q' or event.name == 'esc':
                        console.print("\n[bold red]Shutting down server...[/bold red]")
                        import os
                        os._exit(0)
        except ImportError:
            # Fallback if keyboard module is not working
            console.print("[bold yellow]Note: 'keyboard' module not available. You'll need to manually open the URL in your browser.[/bold yellow]")
            # Start a simple input thread as fallback
            try:
                while True:
                    user_input = input().strip().lower()
                    if user_input == 'o' and not browser_opened:
                        webbrowser.open(local_url)
                        browser_opened = True
                        console.print("[bold green]✓ Browser opened successfully![/bold green]")
                        console.print("[bold yellow]Browser already opened. Press Ctrl+C to exit.[/bold yellow]")
                    elif user_input == 'q' or user_input == 'quit':
                        console.print("[bold red]Shutting down server...[/bold red]")
                        break
            except (KeyboardInterrupt, EOFError):
                pass

    # Start the keypress listener in a separate thread
    key_thread = threading.Thread(target=check_keypress, daemon=True)
    key_thread.start()

    # Suppress Flask/Werkzeug logs for cleaner output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # Suppress werkzeug logs

    # Run the Flask server with minimal output
    socketio.run(app, host='0.0.0.0', port=port, debug=False, use_reloader=False,
                log_output=False)  # Suppress server logs

if __name__ == '__main__':
    run_gui()
