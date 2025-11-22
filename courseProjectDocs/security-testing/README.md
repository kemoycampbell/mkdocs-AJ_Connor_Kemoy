# Security Testing Configuration and Execution
This document outlines the configuration and execution of security testing for the MkDocs project using SonarQube. This setup is exactly the same as the static analysis setup, with the report detailing the security-specific findings.

## Tools
- **SonarQube Community Edition** – Static code analysis platform  
- **PostgreSQL** – Database backend for SonarQube  
- **SonarScanner** – CLI tool to analyze your project’s source code  
- **Docker** – Containerized environment for consistent setup  

**System Configuration**

Similar to the static analysis setup, this report uses **Docker Compose** to:

- Deploy SonarQube and PostgreSQL containers
- Automatically initialize SonarQube and generate an authentication token
- Append the token to the `.env` file for later use by the scanner

## 🔧 Workflow

1.  **Setting up the .env file**

    ```bash
    cp .env.example .env 
    ```

2.  **Configuring the permission**

    ```bash
    sudo chown -R 1000:1000 .
    ```

3.  **Run the docker compose to configure the tools**
    *quirk: If you are running this for the first time, you will need to run it twice as the first run generate the sonar token*

    ```bash
    docker compose up -d
    ```

4.  **View SonarQube Results**

    ```bash
    visit http://localhost:9888 in the browser
    login with your creds from .env
    ```

5. **Re-running the Scan (if needed)**
    
    To re-run the scanner use:

    ```bash
    docker compose run --rm sonarscanner
    ```
