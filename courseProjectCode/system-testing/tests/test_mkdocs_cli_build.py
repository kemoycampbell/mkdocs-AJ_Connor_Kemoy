
from pathlib import Path
import subprocess
from textwrap import dedent
from bs4 import BeautifulSoup


def test_mkdocs_cli_build(tmp_path):
    # Create a temporary mkdocs project
    tmp_dir: Path = tmp_path / "mkdocs_test"
    tmp_dir.mkdir()
    mkdocs_yml: Path = tmp_dir / "mkdocs.yml"
    mkdocs_yml.write_text(dedent("""
                                site_name: Test Site
                                nav:
                                    - Home: index.md
                                    - About: about.md
                                """))
    # Create the docs directory
    docs_dir: Path = tmp_dir / "docs"
    docs_dir.mkdir()
    # Create markdown files
    index_md: Path = docs_dir / "index.md"
    index_md.write_text("# This is the h1 for the home page\n\nThis is the home page paragraph")
    about_md: Path = docs_dir / "about.md"
    about_md.write_text("# This is the h1 for the about page\n\nThis is the about page paragraph")

    # Run mkdocs build via subprocess (black-box)
    cmd = ['mkdocs', 'build', '-f', 'mkdocs.yml', '--use-directory-urls']
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp_dir)

    # Verify the build was successful
    assert result.returncode == 0
    assert (tmp_dir / "site").exists()

    # Verify the generated HTML content
    index_html: Path = tmp_dir / "site" / "index.html"
    assert index_html.exists()
    html_content = index_html.read_text()
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.find('h1')
    assert h1 is not None
    assert h1.get_text() == "This is the h1 for the home page"
    p = soup.find('p')
    assert p is not None
    assert p.get_text() == "This is the home page paragraph"

    about_html: Path = tmp_dir / "site" / "about" / "index.html"
    assert about_html.exists()
    about_content = about_html.read_text()
    about_soup = BeautifulSoup(about_content, 'html.parser')
    about_h1 = about_soup.find('h1')
    assert about_h1 is not None
    assert about_h1.get_text() == "This is the h1 for the about page"
    about_p = about_soup.find('p')
    assert about_p is not None
    assert about_p.get_text() == "This is the about page paragraph"
