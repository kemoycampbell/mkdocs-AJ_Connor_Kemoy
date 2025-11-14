"""
    A black box system test that validate the mkdocs serve command from the cli
    via subproccess.
    It ensures that the server starts correctly and serves the expected content.
"""

import subprocess
import time
import requests


def test_mkdocs_serve(tmp_path):
    #create a temporary directory for the mkdocs project so it can be cleaned up after test
    mkdocs_dir = tmp_path / "mkdocs"
    mkdocs_dir.mkdir()

    #create a new mkdocs project with the new command
    subprocess.run(["mkdocs", "new", "."], cwd=mkdocs_dir, check=True)

    #Start mkdocs serve in background
    process = subprocess.Popen(
        ["mkdocs", "serve", "-a", "0.0.0.0:8000"],
        cwd=mkdocs_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    #wait for the server to start up we will try to connect at least 5 times
    count = 0
    max_retries = 5
    response = None
    while count < max_retries:
        try:
            response = requests.get("http://localhost:8000")
            break     
        except requests.ConnectionError:
            time.sleep(3)
            count += 1
    
    if response is None:
        process.terminate()
        raise Exception("Failed to connect to mkdocs server after multiple attempts")
    
    #check that the response is as expected
    assert response.status_code == 200, "Failed to response with status 200"
    assert "Welcome to MkDocs" in response.text, "Homepage content does not contain Welcome to MkDocs"

    #terminate the mkdocs serve process
    process.send_signal(subprocess.signal.SIGINT)
    process.wait(timeout=5)
    


