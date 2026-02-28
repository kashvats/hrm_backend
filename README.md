# HRMS Lite

## Project Overview
HRMS Lite is a Human Resource Management System built to handle basic personnel management and daily attendance tracking. It consists of a Django-based REST API backend and a React-based single-page frontend application. The system allows administrators to manage employee records, track daily attendance statuses, and view a dashboard summarizing team statistics by department. The application enforces read-only historical attendance, preventing retroactive modifications.

## Tech Stack Used
### Frontend
*   **React** (v18.3+): UI library for building the interface
*   **Vite**: Fast frontend build tool and development server
*   **React Router**: Client-side navigation
*   **Lucide-React**: SVG icon library
*   **Vanilla CSS**: Custom responsive styling with CSS variables

### Backend
*   **Python** (3.11+): Core programming language
*   **Django** (5.0+): High-level Python web framework
*   **Django REST Framework (DRF)**: Toolkit for building the API endpoints
*   **PostgreSQL**: Primary production database (using `psycopg2-binary`)
*   **SQLite**: Development fallback database
*   **Gunicorn**: Python WSGI HTTP Server for UNIX (for production deployment)

## Steps to Run the Project Locally

### Prerequisites
Make sure you have Node.js (for the frontend) and Python 3.11+ (for the backend) installed on your system.

### 1. Backend Setup (`/hrms_backend`)

1.  Navigate into the backend directory:
    ```bash
    cd hrms_backend
    ```
2.  Install system prerequisites (Linux/Ubuntu only):
    ```bash
    sudo apt-get update
    sudo apt-get install python3-venv python3-dev libpq-dev
    ```
3.  Create and activate a Python virtual environment (recommended):
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
4.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Configure Environment Variables:
    *   Create a `.env` file in the `hrms_backend` directory.
    *   Add `SECRET_KEY=your_secret_key` and any custom database credentials if you are using PostgreSQL. If no database variables are provided, SQLite will be used automatically.
6.  Run database migrations:
    ```bash
    python manage.py migrate
    ```
7.  Start the Django development server:
    ```bash
    python manage.py runserver
    ```
    *The API will be available at http://localhost:8000*

### 2. Frontend Setup (`/hrms_frontend`)

1.  Open a **new terminal tab/window**.
2.  Navigate into the frontend directory:
    ```bash
    cd hrms_frontend
    ```
3.  Install Node.js dependencies:
    ```bash
    npm install
    ```
4.  Configure Environment Variables:
    *   Create a `.env` file in the `hrms_frontend` directory.
    *   Set the backend API URL:
        ```env
        VITE_API_URL=http://localhost:8000/api
        ```
5.  Start the Vite development server:
    ```bash
    npm run dev
    ```
    *The frontend will be available at http://localhost:5173*

## Assumptions & Limitations
*   **Authentication**: The current version assumes an internal or administrative environment where explicit user login/authentication is not required.
*   **Historical Data**: Attendance can only be marked for the *current* date. Historical dates are strictly read-only by design.
*   **Deployment**: The repository is pre-configured for deployment on Railway (Nixpacks builder) and Vercel. Moving to other platforms may require adjusting the `Procfile` or build settings.
*   **Data Validation**: Employee IDs must be unique. The system assumes department names are typed consistently (e.g., "Engineering" vs "engineering") as they are currently filtered via exact match.
