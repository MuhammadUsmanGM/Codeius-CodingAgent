"""
Basic tests for the coding agent
"""
import pytest
from coding_agent.agent import CodingAgent
import sys
import os

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


def test_agent_initialization():
    """Test that the agent initializes properly with providers"""
    agent = CodingAgent()
    assert agent.providers is not None
    assert len(agent.providers) >= 1  # Should have at least one provider
    assert agent.conversation_manager.history == []


def test_system_prompt():
    """Test that system prompt is returned properly"""
    agent = CodingAgent()
    prompt = agent.system_prompt()
    assert "Codeius AI Agent Instructions" in prompt
    assert "read_file" in prompt
    assert "write_file" in prompt
    assert "git_commit" in prompt
    assert "web_search" in prompt


def test_get_available_models():
    """Test model listing functionality"""
    agent = CodingAgent()
    models = agent.get_available_models()
    assert isinstance(models, dict)
    assert len(models) >= 1  # Should have at least one model


def test_run_test_command_not_found(capsys):
    """Test the /run_test command with a file that does not exist"""
    from coding_agent.cli import run_test
    run_test("non_existent_file.py")
    captured = capsys.readouterr()
    assert "Test file not found" in captured.out


if __name__ == "__main__":
    pytest.main()