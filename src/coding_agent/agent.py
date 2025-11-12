# src/agent.py

import json
from coding_agent.provider.multiprovider import MultiProvider
from coding_agent.provider.groq import GroqProvider
from coding_agent.provider.google import GoogleProvider
from coding_agent.provider.tavily import TavilyWebSearch
from coding_agent.file_ops import FileOps
from coding_agent.git_ops import GitOps
from dotenv import load_dotenv
load_dotenv()

class CodingAgent:
    def __init__(self):
        self.providers = [GroqProvider(), GoogleProvider()]
        self.llm = MultiProvider(self.providers)
        self.file_ops = FileOps()
        self.git_ops = GitOps()
        self.web_search = TavilyWebSearch()
        self.history = []
        
    def get_current_model_info(self):
        """Get information about the currently active provider/model"""
        if hasattr(self.llm, 'current') and hasattr(self.llm, 'providers'):
            current_idx = self.llm.current
            if 0 <= current_idx < len(self.providers):
                provider = self.providers[current_idx]
                model_name = getattr(provider, 'model', 'unknown')
                provider_name = type(provider).__name__.replace('Provider', '')
                return {
                    'index': current_idx,
                    'name': model_name,
                    'provider': provider_name,
                    'key': f"{provider_name.lower()}_{current_idx}"
                }
        return None
        
    def get_available_models(self):
        """Get list of available models from all providers"""
        models = {}
        for i, provider in enumerate(self.providers):
            # Extract model information from each provider
            model_name = getattr(provider, 'model', 'unknown')
            provider_name = type(provider).__name__.replace('Provider', '')
            models[f"{provider_name.lower()}_{i}"] = {
                'name': model_name,
                'provider': provider_name,
                'instance': provider
            }
        return models
        
    def switch_model(self, model_key):
        """Switch to a specific model by key"""
        models = self.get_available_models()
        if model_key in models:
            # Find the provider index corresponding to the model key
            for i, provider in enumerate(self.providers):
                provider_name = type(provider).__name__.replace('Provider', '')
                current_key = f"{provider_name.lower()}_{i}"
                if current_key == model_key:
                    # Set the specific provider in the MultiProvider
                    self.llm.set_provider(i)
                    return f"Switched to {models[model_key]['name']} ({models[model_key]['provider']})"
        return f"Model {model_key} not found. Use /models to see available models."

    def system_prompt(self):
        return (
            "You are an advanced AI coding agent with the following tools:\n"
            "- Read and write source files in the workspace\n"
            "- Perform git operations (stage, commit)\n"
            "- Perform real-time web searches via a search API\n"
            "When you need to take action, reply with JSON using this structure:\n"
            "{\n"
            " \"explanation\": \"Describe your plan\",\n"
            " \"actions\": [\n"
            "   {\"type\": \"read_file\",  \"path\": \"...\"},\n"
            "   {\"type\": \"write_file\", \"path\": \"...\", \"content\": \"...\"},\n"
            "   {\"type\": \"git_commit\", \"message\": \"...\"},\n"
            "   {\"type\": \"web_search\", \"query\": \"...\"}\n"
            " ]\n"
            "}\n"
            "If only a conversation or non-code answer is needed, reply conversationally."
        )

    def ask(self, prompt, max_tokens=2048):
        # Compose dialogue for LLM
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages += self.history + [{"role": "user", "content": prompt}]
        # Get LLM response
        reply = self.llm.chat(messages, max_tokens)
        # Try to parse/action JSON; else conversational reply
        result, performed = self._try_parse_and_execute(reply)
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": result if performed else reply})
        return result if performed else reply

    def _try_parse_and_execute(self, reply):
        try:
            # Extract JSON from LLM reply (even in markdown code blocks)
            start = reply.find("{")
            end = reply.rfind("}") + 1
            json_str = reply[start:end]
            out = json.loads(json_str)
            actions = out.get("actions", [])
            results = [f"**Agent Plan:** {out.get('explanation', '')}\n"]
            for action in actions:
                if action["type"] == "read_file":
                    content = self.file_ops.read_file(action["path"])
                    results.append(f"🔹 Read `{action['path']}`:\n``````")
                elif action["type"] == "write_file":
                    res = self.file_ops.write_file(action["path"], action["content"])
                    results.append(f"✅ Wrote `{action['path']}`.")
                elif action["type"] == "git_commit":
                    self.git_ops.stage_files(".")
                    cm = self.git_ops.commit(action["message"])
                    results.append(f"✅ Git commit: {action['message']}")
                elif action["type"] == "web_search":
                    answer = self.web_search.search(action["query"])
                    results.append(f"🌐 Web search for '{action['query']}':\n{answer}\n")
            return "\n".join(results), True
        except Exception:
            return reply, False

    def reset_history(self):
        self.history = []
