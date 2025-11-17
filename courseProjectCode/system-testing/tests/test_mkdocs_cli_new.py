"""
System Tests for MkDocs

Black-box system tests that validate end-to-end workflows through the CLI interface.
These tests use subprocess to invoke MkDocs commands without importing internal modules.
"""

import subprocess
import tempfile
import os


def test_mkdocs_new_creates_project():
    """
    System Test 1: New Project Creation Workflow

    Tests that 'mkdocs new <project>' creates a complete project structure
    with default configuration and documentation files.
    """
    with tempfile.TemporaryDirectory(prefix='mkdocs_system_test_') as temp_dir:
        project_name = "test_project"
        project_path = os.path.join(temp_dir, project_name)

        # Execute mkdocs new via subprocess (black-box)
        result = subprocess.run(
            ['mkdocs', 'new', project_name],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )

        # Verify command executed successfully
        assert result.returncode == 0, f"mkdocs new failed: {result.stderr}"
        
        # Verify project structure
        assert os.path.exists(project_path), "Project directory not created"
        assert os.path.isfile(os.path.join(project_path, 'mkdocs.yml')), "mkdocs.yml not created"
        assert os.path.isdir(os.path.join(project_path, 'docs')), "docs/ directory not created"
        assert os.path.isfile(os.path.join(project_path, 'docs', 'index.md')), "docs/index.md not created"

        # Verify mkdocs.yml contains default site name
        with open(os.path.join(project_path, 'mkdocs.yml'), 'r') as f:
            config_content = f.read()
            assert 'site_name: My Docs' in config_content, "Default site_name not found in config"

        # Verify docs/index.md contains welcome content
        with open(os.path.join(project_path, 'docs', 'index.md'), 'r') as f:
            index_content = f.read()
            assert '# Welcome to MkDocs' in index_content, "Welcome header not found in index.md"
            assert 'mkdocs new [dir-name]' in index_content, "Command documentation not found"
