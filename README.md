# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS
- FastAPI (Python)
- SQLAlchemy
- scikit-learn
- NLTK

## Backend Setup

The backend is a Python application built with FastAPI.

### Prerequisites

- Python 3.8+
- pip

### Installation

1.  **Navigate to the backend directory:**
    ```sh
    cd backend
    ```

2.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Backend

1.  **Start the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```
    The server will be running at `http://127.0.0.1:8000`.

## Features

This project is an implementation of the Autonomous SaaS Organism blueprint. It includes the following core components:

*   **Sense Engine:** Scrapes websites to gather raw data about human problems.
*   **Decision Core:** Analyzes the collected data using TF-IDF, KMeans clustering, and sentiment analysis to identify potential SaaS ideas.
*   **API:** Exposes endpoints to trigger the Sense Engine and retrieve ideas from the Decision Core.
*   **Frontend:** A React application to interact with the backend, trigger scraping, and view the generated ideas.


## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
