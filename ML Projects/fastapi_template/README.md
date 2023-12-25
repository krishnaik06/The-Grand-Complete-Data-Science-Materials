# FastAPI Template with Advanced Features

This repository provides a FastAPI template with a modular folder structure and several advanced features to help you kickstart your web API project. It includes custom OAuth2 JWT token authentication, integration with Azure Key Vault for secure configuration management, Microsoft SQL Server database connection using stored procedures, API versioning, robust exception handling, and logging into Microsoft SQL Server. Additionally, Docker support is included to simplify deployment.

## Features

- **Modular Folder Structure**: The project follows a modular structure, making it easy to organize and scale your application.

- **Custom OAuth2 JWT Token**: Secure your API endpoints with OAuth2 JWT token authentication, ensuring that only authorized users can access protected resources.

- **Azure Key Vault Integration**: Safely manage sensitive configurations and secrets using Azure Key Vault to ensure your application's security.

- **Microsoft SQL Server Database**: Connect to Microsoft SQL Server and utilize stored procedures for efficient data access and management.

- **API Versioning**: Implement API versioning to ensure backward compatibility as your API evolves.

- **Exception Handling**: Comprehensive exception handling is integrated to gracefully handle errors and provide meaningful responses to clients.

- **Logging**: Logs are generated and stored in Microsoft SQL Server for easy monitoring and troubleshooting.

- **Docker Support**: Dockerfiles and Docker Compose files are included to simplify the deployment process.

## Getting Started

Follow these steps to get started with the FastAPI template:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/MusaddiqueHussainLabs/fastapi_template.git
   cd fastapi_template
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure Azure Key Vault:
   - Set up an Azure Key Vault instance and configure the necessary secrets and configurations for your application.
   - Update the `config.py` file with your Azure Key Vault settings.

4. Configure Microsoft SQL Server:
   - Update the `config.py` file with your Microsoft SQL Server database connection details.
   - Ensure that the necessary stored procedures are created in your database.

5. Run the FastAPI application:

   ```bash
   uvicorn app.main:app --host localhost --port 8080 --reload
   ```

6. Access the API at `http://localhost:8080`.

## MS SQL
You can find create table and stored Procedure scripts under "references" folder

**Note:** You need to configure your development environment with the prerequisites in order to develop an application using the pyodbc Python driver for SQL Server.

[Install the ODBC driver for windows](https://learn.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver16&tabs=windows#install-the-odbc-driver)

## API Documentation

API documentation is automatically generated using [Swagger UI](https://swagger.io/tools/swagger-ui/) and is available at `http://localhost:8080/docs` or `http://localhost:8080/redoc`.

## Docker Support

To run the application in a Docker container, use the provided Dockerfiles and Docker Compose files:

1. Build the Docker image:

   ```bash
   docker-compose build
   ```

2. Start the Docker container:

   ```bash
   docker-compose up -d
   ```

## Contribution

Contributions are welcome! Please feel free to open issues or submit pull requests to improve this template.

## License

This project is licensed under the [MIT License](LICENSE.md).

---

**Happy coding!** 🚀