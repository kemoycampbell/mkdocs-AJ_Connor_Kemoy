import subprocess
import time
import os
import shutil
import tempfile
import json
import psutil
import pandas as pd
from datetime import datetime

class RealWorldMkDocsLoadTester:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def clone_and_test_repo(self, repo_url, name, branch="main"):
        """Clone a real repo and test its build performance."""
        print(f"Testing: {name}")
        print(f"Repo: {repo_url}")

        # Create temp directory
        temp_dir = tempfile.mkdtemp(prefix=f"mkdocs_test_{name}_")
        print(f"Working directory: {temp_dir}")

        try:
            # Clone the repo
            print("Cloning repository...")
            clone_start = time.time()
            subprocess.run(
                ["git", "clone", "--depth", "1", "-b", branch, repo_url, temp_dir],
                capture_output=True,
                check=True
            )
            clone_time = time.time() - clone_start
            print(f"Cloned in {clone_time:.2f}s")

            # Find mkdocs.yml
            mkdocs_config = self.find_mkdocs_config(temp_dir)
            if not mkdocs_config:
                print(f"⚠️  No mkdocs.yml found in {name}")
                return None

            project_dir = os.path.dirname(mkdocs_config)
            print(f"Project directory: {project_dir}")

            # Analyze the project
            project_stats = self.analyze_project(project_dir)
            print(f"Project stats: {json.dumps(project_stats, indent=2)}")

            # Run build tests
            build_results = self.run_build_tests(project_dir, name)

            # Combine results
            result = {
                'name': name,
                'repo': repo_url,
                'project_stats': project_stats,
                'build_results': build_results,
                'clone_time': clone_time
            }

            self.results.append(result)
            return result

        except subprocess.CalledProcessError as e:
            print(f"❌ Error cloning {name}: {e}")
            return None
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def find_mkdocs_config(self, directory):
        """Find mkdocs.yml or mkdocs.yaml."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file in ['mkdocs.yml', 'mkdocs.yaml']:
                    return os.path.join(root, file)
        return None

    def analyze_project(self, project_dir):
        """Analyze project structure and complexity."""
        stats = {
            'total_pages': 0,
            'markdown_files': 0,
            'image_files': 0,
            'css_files': 0,
            'js_files': 0,
            'total_size_mb': 0,
            'plugins': [],
            'theme': None
        }

        docs_dir = os.path.join(project_dir, "docs")
        if not os.path.exists(docs_dir):
            # Try to find docs directory
            for root, dirs, files in os.walk(project_dir):
                if 'docs' in dirs:
                    docs_dir = os.path.join(root, 'docs')
                    break

        if os.path.exists(docs_dir):
            for root, dirs, files in os.walk(docs_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    stats['total_size_mb'] += size / (1024 * 1024)

                    if file.endswith('.md'):
                        stats['markdown_files'] += 1
                        stats['total_pages'] += 1
                    elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                        stats['image_files'] += 1
                    elif file.endswith('.css'):
                        stats['css_files'] += 1
                    elif file.endswith('.js'):
                        stats['js_files'] += 1

        # Parse mkdocs.yml for plugins and theme
        config_path = os.path.join(project_dir, "mkdocs.yml")
        if os.path.exists(config_path):
            with open(config_path) as f:
                content = f.read()
                # Simple parsing (could use PyYAML for better parsing)
                if 'plugins:' in content:
                    stats['plugins'] = ['plugins_detected']
                if 'theme:' in content:
                    stats['theme'] = 'custom'

        return stats

    def run_build_tests(self, project_dir, name):
        """Run comprehensive build tests."""
        results = []

        tests = [
            ("clean_build", ["mkdocs", "build", "--clean"]),
            ("dirty_build", ["mkdocs", "build", "--dirty"]),
            ("verbose_build", ["mkdocs", "build", "--verbose"]),
            ("strict_build", ["mkdocs", "build", "--strict"]),
        ]

        for test_name, command in tests:
            print(f"\nRunning {test_name}...")

            # Warm up (first run)
            subprocess.run(
                command,
                cwd=project_dir,
                capture_output=True
            )

            # Measure performance
            build_times = []
            memory_usages = []

            for i in range(3):  # Multiple runs for consistency
                # Get memory before
                process = psutil.Process()
                memory_before = process.memory_info().rss / 1024 / 1024  # MB

                # Run build
                start_time = time.time()
                result = subprocess.run(
                    command,
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )
                elapsed = time.time() - start_time

                # Get memory after
                memory_after = process.memory_info().rss / 1024 / 1024
                memory_used = memory_after - memory_before

                build_times.append(elapsed)
                memory_usages.append(memory_used)

                if result.returncode != 0:
                    print(f"⚠️  Build failed: {result.stderr[:200]}")

            avg_time = sum(build_times) / len(build_times)
            avg_memory = sum(memory_usages) / len(memory_usages)

            test_result = {
                'test': test_name,
                'avg_time_seconds': round(avg_time, 2),
                'avg_memory_mb': round(avg_memory, 2),
                'min_time': round(min(build_times), 2),
                'max_time': round(max(build_times), 2),
                'success': result.returncode == 0
            }

            results.append(test_result)
            print(f"  Result: {test_result}")

        return results

    def compare_repositories(self):
        """Compare performance across different repositories."""
        print("\n" + "="*60)
        print("COMPARATIVE ANALYSIS")
        print("="*60)

        comparison_data = []

        for result in self.results:
            if not result:
                continue

            # Get the clean build result
            clean_build = None
            for build in result['build_results']:
                if build['test'] == 'clean_build':
                    clean_build = build
                    break

            if clean_build:
                comparison_data.append({
                    'Repository': result['name'],
                    'Pages': result['project_stats']['total_pages'],
                    'Markdown Files': result['project_stats']['markdown_files'],
                    'Images': result['project_stats']['image_files'],
                    'Total Size (MB)': round(result['project_stats']['total_size_mb'], 2),
                    'Build Time (s)': clean_build['avg_time_seconds'],
                    'Memory Used (MB)': clean_build['avg_memory_mb'],
                    'Time per Page (ms)': (clean_build['avg_time_seconds'] * 1000) /
                                         max(1, result['project_stats']['total_pages']),
                    'Has Plugins': len(result['project_stats']['plugins']) > 0
                })

        # Create DataFrame for analysis
        df = pd.DataFrame(comparison_data)

        if not df.empty:
            print("\n📊 Performance Comparison:")
            print(df.to_string(index=False))

            # Save to CSV
            csv_file = f"mkdocs_comparison_{self.timestamp}.csv"
            df.to_csv(csv_file, index=False)
            print(f"\n✅ Comparison saved to: {csv_file}")

            # Generate insights
            self.generate_insights(df)

        return df

    def generate_insights(self, df):
        """Generate actionable insights from comparison"""
        print("\n" + "="*60)
        print("KEY INSIGHTS")
        print("="*60)

        insights = []

        # Time per page analysis
        avg_time_per_page = df['Time per Page (ms)'].mean()
        insights.append(f"• Average time per page: {avg_time_per_page:.1f}ms")

        # Identify outliers
        max_time_page = df.loc[df['Time per Page (ms)'].idxmax()]
        insights.append(f"• Slowest per-page performance: {max_time_page['Repository']} "
                       f"({max_time_page['Time per Page (ms)']:.1f}ms/page)")

        # Memory efficiency
        memory_per_page = []
        for _, row in df.iterrows():
            if row['Pages'] > 0:
                memory_per_page.append(row['Memory Used (MB)'] / row['Pages'])

        if memory_per_page:
            avg_memory_per_page = sum(memory_per_page) / len(memory_per_page)
            insights.append(f"• Average memory per page: {avg_memory_per_page:.2f} MB/page")

        # Plugin impact (if we have that data)
        if 'Has Plugins' in df.columns:
            with_plugins = df[df['Has Plugins'] == True]
            without_plugins = df[df['Has Plugins'] == False]

            if not with_plugins.empty and not without_plugins.empty:
                avg_with = with_plugins['Time per Page (ms)'].mean()
                avg_without = without_plugins['Time per Page (ms)'].mean()
                plugin_impact = ((avg_with - avg_without) / avg_without) * 100
                insights.append(f"• Plugin impact: +{plugin_impact:.1f}% build time per page")

        # Print insights
        for insight in insights:
            print(insight)

        # Save insights
        with open(f"insights_{self.timestamp}.md", "w") as f:
            f.write("# MkDocs Performance Insights\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Key Findings\n\n")
            for insight in insights:
                f.write(f"{insight}\n")

# Main execution
if __name__ == "__main__":
    tester = RealWorldMkDocsLoadTester()

    # Test real repositories
    repos = [
        "mkdocs/",
        "terraform-provider-cdk-docs/"
        # {
        #     "url": "https://github.com/squidfunk/mkdocs-material.git",
        #     "name": "Material for MkDocs",
        #     "branch": "master"
        # },
        # {
        #     "url": "https://github.com/tiangolo/fastapi.git",
        #     "name": "FastAPI Docs",
        #     "branch": "main"
        # }
    ]

    for repo in repos:
        tester.clone_and_test_repo(repo["url"], repo["name"], repo.get("branch", "main"))

    # Compare results
    comparison_df = tester.compare_repositories()

    print("\n✅ Load testing complete!")
    print(f"Results saved with timestamp: {tester.timestamp}")
