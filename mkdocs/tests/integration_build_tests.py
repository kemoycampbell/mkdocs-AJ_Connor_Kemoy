import textwrap
from pathlib import Path
from unittest import mock
import jinja2

from mkdocs.config import config_options as c
from mkdocs.config import load_config
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import _build_template
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation
from mkdocs.contrib.search import SearchPlugin

class _FakePluginConfig(Config):
    author = c.Type(str, default='AJ Connor Kemoy')
    version = c.Type(str, default='1.0.0')
    dir = c.Optional(c.Dir(exists=False))

class FakePlugin(BasePlugin[_FakePluginConfig]):
    def on_post_template(
        self, output_content: str, *, template_name: str, config
    ) -> str:
        # add a <footer> tag at the end before the closing html tag
        footer_content = f"\n<footer><p>Plugin Footer: {self.config.author}, {self.config.version}</p></footer>\n"
        return output_content.replace("</html>", f"\t{footer_content}\n</html>")

class FakeEntryPoint:
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls

    def load(self):
        return self.cls

class TestBuildTemplateWithPlugin:
    @mock.patch(
        'mkdocs.plugins.entry_points',
        mock.Mock(
            return_value=[
                FakeEntryPoint('sample', FakePlugin),
                FakeEntryPoint('search', SearchPlugin),  # placeholder for other plugins
            ]
        ),
    )
    def test_build_template_with_plugin(self, tmp_path):
        #TESTING DATA
        SITE_NAME = "Test Site"
        SITE_URL = "http://localhost:8080"
        NAVIGATIONS = [
            {"title": "Home", "file": "index.md"},
            {"title": "About", "file": "about.md"},
            {"title": "Contact", "file": "contact.md"},
        ]

        #create  mkdoc project structure in a temporary directory
        docs_dir: Path = tmp_path / "docs"
        docs_dir.mkdir()

        #list of navigation items
        (docs_dir / "index.md").write_text("# Home Page")
        (docs_dir / "about.md").write_text("# About Page")
        (docs_dir / "contact.md").write_text("# Contact Page")

        #create mkdocs config file
        config_file: Path = tmp_path / "mkdocs.yml"

        config_file.write_text(textwrap.dedent(f"""
            site_name: {SITE_NAME}
            site_url: {SITE_URL}
            nav:
            - Home: index.md
            - About: about.md
            - Contact: contact.md
            plugins:
            - sample:
                author: AJ Connor Kemoy
                version: 1.0.0
        """))

        # load the config
        config = load_config(str(config_file))

        # assertIsInstance(config.plugins, PluginCollection)
        # self.assertIn('sample', config.plugins)

        # simple Jinja2 template
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

        files = get_files(config)
        nav = get_navigation(files, config)

        generated_html = _build_template(
            name="index.html",
            template=template_content,
            files=files,
            config=config,
            nav=nav
        )

        #assert that we have what we expected
        assert f"<h1>Welcome to {SITE_NAME}</h1>" in generated_html
        assert f"<title>{SITE_NAME}</title>" in generated_html

        #ensure all nav items are present
        for item in NAVIGATIONS:
            assert f"<li>{item['title']}</li>" in generated_html

        #ensure plugin footer is present
        assert "<footer><p>Plugin Footer: AJ Connor Kemoy, 1.0.0</p></footer>" in generated_html

class TestBuildTemplate:
    def test_build_template(self, tmp_path):
        #TESTING DATA
        SITE_NAME = "Test Site"
        SITE_URL = "http://localhost:8080"
        NAVIGATIONS = [
            {"title": "Home", "file": "index.md"},
            {"title": "About", "file": "about.md"},
            {"title": "Contact", "file": "contact.md"},
        ]

        #create  mkdoc project structure in a temporary directory
        docs_dir: Path = tmp_path / "docs"
        docs_dir.mkdir()

        #list of navigation items
        (docs_dir / "index.md").write_text("# Home Page")
        (docs_dir / "about.md").write_text("# About Page")
        (docs_dir / "contact.md").write_text("# Contact Page")

        #create mkdocs config file
        config_file: Path = tmp_path / "mkdocs.yml"

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

        #assert that we have what we expected
        assert f"<h1>Welcome to {SITE_NAME}</h1>" in generated_html
        assert f"<title>{SITE_NAME}</title>" in generated_html

        #ensure all nav items are present
        for item in NAVIGATIONS:
            assert f"<li>{item['title']}</li>" in generated_html


def test_missing_nav_files(tmp_path):
    """Test integration behavior when navigation references non-existent files"""

    #create mkdocs project structure with docs directory
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    #only create index.md, but nav will reference other files
    (docs_dir / "index.md").write_text("# Home Page")

    #create config that references files that don't exist
    config_file = tmp_path / "mkdocs.yml"
    config_file.write_text(textwrap.dedent("""
        site_name: Test Site
        site_url: http://localhost:8080
        nav:
        - Home: index.md
        - About: about.md
        - Contact: contact.md
    """))

    #load config - should succeed even with missing files referenced
    config = load_config(config_file=str(config_file))

    #get_files should only find index.md
    files = get_files(config)

    #verify only one file was found
    file_list = list(files)
    assert len(file_list) == 1
    assert file_list[0].src_path == "index.md"

    #get_navigation should handle missing files gracefully
    nav = get_navigation(files, config)

    #verify navigation was created but only contains existing pages
    assert nav is not None
    assert len(nav.pages) == 1
    assert nav.pages[0].title == "Home"
