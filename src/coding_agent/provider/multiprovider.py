# src/providers/multiprovider.py

class MultiProvider:
    """
    Wrapper to automatically switch between LLM providers on quota/rate failures.
    """
    def __init__(self, providers):
        self.providers = providers  # [GroqProvider(), GoogleProvider()]
        self.current = 0

    def chat(self, messages, max_tokens=2048):
        tried = 0
        last_exception = None
        total = len(self.providers)
        while tried < total:
            try:
                return self.providers[self.current].chat(messages, max_tokens)
            except RuntimeError as e:
                last_exception = e
                self.current = (self.current + 1) % total
                tried += 1
        raise RuntimeError(f"All providers failed: {last_exception}")
