import tempfile
import textwrap
from pathlib import Path
import jinja2

from mkdocs.config import load_config
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.commands.build import _build_template
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation
import unittest



def test_build_template(tmp_path):
    #TESTING DATA
    SITE_NAME = "Test Site"
    SITE_URL = "http://localhost:8080"
    NAVIGATIONS = [
        {"title": "Home", "file": "index.md"},
        {"title": "About", "file": "about.md"},
        {"title": "Contact", "file": "contact.md"},
    ]

    #create  mkdoc project structure in a temporary directory
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    #list of navigation items
    (docs_dir / "index.md").write_text("# Home Page")
    (docs_dir / "about.md").write_text("# About Page")
    (docs_dir / "contact.md").write_text("# Contact Page")

    #create mkdocs config file
    config_file = tmp_path / "mkdocs.yml"

    config_file.write_text(textwrap.dedent(f"""
        site_name: {SITE_NAME}
        site_url: {SITE_URL}
        nav:
        - Home: index.md
        - About: about.md
        - Contact: contact.md
    """))

    #load the config
    config = load_config(config_file=str(config_file))

    #simple Jinja2 template
    template_content = jinja2.Template("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{{ config.site_name }}</title>
        </head>
        <body>
            <h1>Welcome to {{ config.site_name }}</h1>
            {% for page in nav.pages %}
                <li>{{ page.title }}</li>
            {% endfor %}
        </body>
    </html>
    """)

    #empty files and navigations as we dont want to test those since I am already testing config and template rendering
    files = get_files(config)
    nav = get_navigation(files, config)

    #build the template
    generated_html = _build_template(
        name="index.html",
        template=template_content,
        files=files,
        config=config,
        nav=nav
    )
    print(generated_html)

    #assert that we have what we expected
    assert f"<h1>Welcome to {SITE_NAME}</h1>" in generated_html
    assert f"<title>{SITE_NAME}</title>" in generated_html

    #ensure all nav items are present
    for item in NAVIGATIONS:
        assert f"<li>{item['title']}</li>" in generated_html
