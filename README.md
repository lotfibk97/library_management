# Library Management System

A FastAPI-based library management system using PostgreSQL for user authentication, book management, and borrowing functionality.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (with Docker Compose) installed.

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/lotfibk97/library_management.git
   cd library_management
   ```

2. **Run the Application**

   ```bash
   docker-compose up --build
   ```

   This command:
   - Builds and starts the FastAPI app at `http://localhost:8000`.
   - Starts a PostgreSQL database in a Docker container.
   - Requires no local PostgreSQL installation.

3. **Access the API**

   - Open `http://localhost:8000/docs` in a browser to access the interactive Swagger UI.
   - Example endpoints:
     - `POST /users/` - Register a user.
     - `POST /books/` - Create a book (librarian only).
     - `POST /borrowing/borrow` - Borrow a book.

4. **Run Tests**

   ```bash
   docker-compose exec app pytest
   ```

   This runs the test suite to verify functionality.

## Stopping the Application

- **Stop**: Press `Ctrl+C` in the terminal.
- **Remove Containers**: Run:

   ```bash
   docker-compose down
   ```

## Notes

- **Database**: PostgreSQL runs in a Docker container with persistent data storage.
- **Configuration**: The `DATABASE_URL` is set in `docker-compose.yml` to connect to the containerized database.
- **Dependencies**: All Python dependencies are installed automatically in the Docker image.

## Troubleshooting

- Ensure Docker is running before executing `docker-compose up`.
- If tests fail, check logs with:

   ```bash
   docker-compose logs app
   docker-compose logs db
   ```

- For further help, consult the [FastAPI documentation](https://fastapi.tiangolo.com/) or [PostgreSQL Docker documentation](https://hub.docker.com/_/postgres).
