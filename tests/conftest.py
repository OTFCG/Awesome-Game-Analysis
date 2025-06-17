"""Shared pytest fixtures and configuration for all tests."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_toml_file(temp_dir: Path) -> Path:
    """Create a mock TOML file for testing."""
    toml_file = temp_dir / "test_games.toml"
    toml_content = """
[[game]]
name = "Test Game"
url = "https://github.com/test/game"
description = "A test game for unit testing"
tags = ["test", "mock"]

[[game]]
name = "Another Test Game"
url = "https://github.com/test/another-game"
description = "Another test game"
tags = ["test", "example"]
"""
    toml_file.write_text(toml_content)
    return toml_file


@pytest.fixture
def mock_markdown_file(temp_dir: Path) -> Path:
    """Create a mock Markdown file for testing."""
    md_file = temp_dir / "test.md"
    md_content = """# Test Markdown

This is a test markdown file.

## Section 1

Some content here.

## Section 2

More content here.
"""
    md_file.write_text(md_content)
    return md_file


@pytest.fixture
def mock_config() -> dict:
    """Provide a mock configuration dictionary."""
    return {
        "input_file": "games.toml",
        "output_file": "README.md",
        "preface_file": "preface.md",
        "epilogue_file": "epilogue.md",
        "references_file": "references.md",
        "debug": False,
    }


@pytest.fixture
def mock_game_data() -> list[dict]:
    """Provide mock game data for testing."""
    return [
        {
            "name": "PyGame Example",
            "url": "https://github.com/pygame/pygame",
            "description": "A popular Python game development library",
            "tags": ["library", "game-engine"],
        },
        {
            "name": "Python Snake",
            "url": "https://github.com/example/snake",
            "description": "Classic snake game in Python",
            "tags": ["arcade", "classic"],
        },
        {
            "name": "Chess AI",
            "url": "https://github.com/example/chess",
            "description": "Chess game with AI opponent",
            "tags": ["strategy", "ai"],
        },
    ]


@pytest.fixture(autouse=True)
def change_test_dir(temp_dir: Path, monkeypatch):
    """Automatically change to temp directory for each test."""
    monkeypatch.chdir(temp_dir)


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get for testing HTTP calls."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"stargazers_count": 100}
    mock_response.text = "Mock response text"
    
    mock_get = mocker.patch("requests.get", return_value=mock_response)
    return mock_get


@pytest.fixture
def capture_stdout():
    """Capture stdout for testing print statements."""
    import io
    import sys
    
    original_stdout = sys.stdout
    captured_output = io.StringIO()
    
    class CaptureManager:
        def start(self):
            sys.stdout = captured_output
        
        def stop(self):
            sys.stdout = original_stdout
        
        def getvalue(self):
            return captured_output.getvalue()
    
    return CaptureManager()


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set mock environment variables for testing."""
    test_env = {
        "TEST_VAR": "test_value",
        "DEBUG": "true",
        "API_KEY": "mock_api_key",
    }
    
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    return test_env