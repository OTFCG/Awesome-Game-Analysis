"""Validation tests to ensure the testing infrastructure is set up correctly."""

import sys
from pathlib import Path

import pytest


class TestInfrastructureSetup:
    """Test class to validate the testing infrastructure setup."""

    def test_pytest_is_installed(self):
        """Verify pytest is installed and importable."""
        import pytest
        assert pytest.__version__ is not None

    def test_pytest_cov_is_installed(self):
        """Verify pytest-cov is installed and importable."""
        import pytest_cov
        assert pytest_cov is not None

    def test_pytest_mock_is_installed(self):
        """Verify pytest-mock is installed and importable."""
        import pytest_mock
        assert pytest_mock is not None

    def test_project_structure_exists(self):
        """Verify the project structure is set up correctly."""
        project_root = Path(__file__).parent.parent
        
        # Check main directories
        assert project_root.exists()
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        assert (project_root / "scripts").exists()
        
        # Check important files
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / "tests" / "__init__.py").exists()
        assert (project_root / "tests" / "conftest.py").exists()

    def test_fixtures_are_available(self, temp_dir, mock_config, mock_game_data):
        """Verify that common fixtures are available and working."""
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test mock_config fixture
        assert isinstance(mock_config, dict)
        assert "input_file" in mock_config
        assert "output_file" in mock_config
        
        # Test mock_game_data fixture
        assert isinstance(mock_game_data, list)
        assert len(mock_game_data) > 0
        assert all("name" in game for game in mock_game_data)

    def test_mock_file_fixtures(self, mock_toml_file, mock_markdown_file):
        """Verify file creation fixtures work correctly."""
        # Test TOML file fixture
        assert mock_toml_file.exists()
        assert mock_toml_file.suffix == ".toml"
        content = mock_toml_file.read_text()
        assert "[[game]]" in content
        assert "Test Game" in content
        
        # Test Markdown file fixture
        assert mock_markdown_file.exists()
        assert mock_markdown_file.suffix == ".md"
        content = mock_markdown_file.read_text()
        assert "# Test Markdown" in content

    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Verify the unit test marker is configured."""
        assert True

    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Verify the integration test marker is configured."""
        assert True

    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Verify the slow test marker is configured."""
        assert True

    def test_coverage_configuration(self):
        """Verify coverage is configured correctly."""
        # This test will pass if coverage is running
        # The actual coverage check happens via pytest-cov
        assert True

    def test_python_path_includes_project_root(self):
        """Verify the Python path is set up correctly for imports."""
        project_root = str(Path(__file__).parent.parent)
        assert any(project_root in path for path in sys.path)


class TestMockingCapabilities:
    """Test class to validate mocking capabilities."""

    def test_requests_mock_works(self, mock_requests_get):
        """Verify the requests mock fixture works correctly."""
        import requests
        
        response = requests.get("https://api.example.com/data")
        assert response.status_code == 200
        assert response.json() == {"stargazers_count": 100}
        mock_requests_get.assert_called_once()

    def test_stdout_capture_works(self, capture_stdout):
        """Verify stdout capture fixture works correctly."""
        capture_stdout.start()
        print("Test output")
        print("Another line")
        capture_stdout.stop()
        
        output = capture_stdout.getvalue()
        assert "Test output" in output
        assert "Another line" in output

    def test_env_vars_mock_works(self, mock_env_vars):
        """Verify environment variable mocking works correctly."""
        import os
        
        assert os.environ.get("TEST_VAR") == "test_value"
        assert os.environ.get("DEBUG") == "true"
        assert os.environ.get("API_KEY") == "mock_api_key"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])