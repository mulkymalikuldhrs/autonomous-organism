# ORGANISME SAAS OTONOM

This project is an autonomous SaaS organism that finds human problems, builds solutions, and deploys them automatically. It is designed to be self-sufficient, open-source, and capable of evolving on its own.

## Getting Started

### Prerequisites

- Node.js & npm
- Python 3.8+ & pip
- Docker (optional)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <YOUR_GIT_URL>
    ```
2.  **Navigate to the project directory:**
    ```sh
    cd <YOUR_PROJECT_NAME>
    ```
3.  **Install frontend dependencies:**
    ```sh
    npm i
    ```
4.  **Install backend dependencies:**
    ```sh
    pip install -r backend/requirements.txt
    ```

### Running the Application

1.  **Start the backend server:**
    ```sh
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
2.  **Start the frontend development server:**
    ```sh
    npm run dev
    ```

## Project Structure

-   `src/`: Frontend source code (React, Vite, shadcn-ui, Tailwind CSS)
-   `backend/`: Backend source code (FastAPI)
-   `blueprint.md`: The technical and philosophical blueprint of the organism.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
