# Autonomous SaaS Organism - Backend

This directory contains the Python backend for the Autonomous SaaS Organism, built with FastAPI.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**
    The application uses a local SQLite database (`organism.db`) which is created automatically when the server starts. No manual setup is needed.

## Running the Server

To run the backend server locally, use the following command from the project's root directory:

```bash
uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`.

## API Endpoints

*   **`POST /api/sense/run`**: Triggers the Sense Engine to scrape for new problems and store them in the database.
