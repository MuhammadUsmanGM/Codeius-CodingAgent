# src/file_ops.py

from pathlib import Path

class FileOps:
    def __init__(self, root="."):
        self.root = Path(root)

    def read_file(self, file_path):
        path = self.root / file_path
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file '{file_path}': {e}"

    def write_file(self, file_path, content):
        path = self.root / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            return f"Error writing file '{file_path}': {e}"

    def list_files(self, pattern="**/*.py"):
        return [str(p.relative_to(self.root)) for p in self.root.glob(pattern) if p.is_file()]
