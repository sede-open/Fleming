# How-To Guide: Generic Frontend for Project Fleming

*(Guide current as of: Monday, April 14, 2025)*

## Introduction

This guide will walk you through:
1.  Prerequisites
2.  Setting up the development environment
3.  Configuring the application to connect to your Project Fleming ML API
4.  Running the application locally
5.  Understanding the basic architecture

## Prerequisites

Before you begin, ensure you have the following installed and available:

1.  **Node.js:** (Version 20.x or later recommended for Next.js). You can download it from [nodejs.org](https://nodejs.org/).
2.  **Package Manager:** `npm` (comes with Node.js), `yarn`, `pnpm`, or `bun`. Choose one you are comfortable with.
3.  **Git:** For cloning the repository.
4.  **Project Fleming ML API Endpoint:** You need the URL where your instance of the Project Fleming ML backend API is running.
5.  **API Authentication Token:** You need the authentication token required to securely access the Project Fleming ML API.

*(You should obtain the ML API endpoint and Auth Token from the team or documentation related to your specific Project Fleming backend deployment.)*

## Getting Started: Setup and Running

Follow these steps to get the frontend running on your local machine:

1.  **Clone the Repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone <repository-url> # Replace <repository-url> with the actual URL of your frontend's Git repository
    cd <repository-directory>   # Navigate into the cloned project folder
    ```

2.  **Install Dependencies:**
    Using your preferred package manager, install the necessary project dependencies:
    ```bash
    # Using npm
    npm install

    # Or using yarn
    yarn install

    # Or using pnpm
    pnpm install

    # Or using bun
    bun install
    ```

3.  **Configure Environment Variables:**
    This application needs to know where the Project Fleming ML API is located and how to authenticate with it.
    * Create a new file named `.env` in the root directory of the project.
    * Open the `.env` file and add the following lines, replacing the placeholder values with your actual API details:

    ```plaintext
    # .env file content

    # The full URL to your Project Fleming ML API endpoint
    ML_API=https://your-project-fleming-api.example.com/api/search

    # The authentication token required by the API
    API_AUTH_TOKEN=your_secret_auth_token_here
    ```
    * **Important:** Ensure the `ML_API` value is the correct endpoint provided by your Project Fleming backend for making search/prediction requests. Save the `.env` file. This file is typically ignored by Git (via `.gitignore`) to keep your secrets safe.

4.  **Run the Development Server:**
    Start the Next.js development server:
    ```bash
    # Using npm
    npm run dev

    # Or using yarn
    yarn dev

    # Or using pnpm
    pnpm dev

    # Or using bun
    bun dev
    ```

5.  **Access the Application:**
    Open your web browser and navigate to:
    `http://localhost:3000`

    You should now see the generic frontend application running.

## How It Works: Architecture Overview

Understanding the flow of data is key to using and potentially customizing this frontend:

1.  **User Interaction:** The user interacts with the UI, likely entering a search query into an input field in the page located at `app/page.tsx`.
2.  **Frontend API Call:** When the user submits their query, the frontend code (in `app/page.tsx` or related components) makes a request to its *own* internal API route: `/api/predictions`.
3.  **Internal API Route (`/api/predictions`):**
    * This Next.js API route (defined in `app/api/predictions/route.ts`) acts as a proxy or intermediary.
    * It receives the request from the frontend UI.
    * It reads the `ML_API` and `API_AUTH_TOKEN` from the environment variables (which you set in the `.env` file).
    * It then makes a secure request (using the auth token) to the actual **Project Fleming ML API** (the URL specified in `ML_API`).
    * It receives the raw prediction data (e.g., list of repos, articles) from the ML API.
    * It perform some basic processing or reformatting on this data to make it suitable for the frontend UI.
    * It sends the processed data back as a response to the frontend UI component that initially called it.
4.  **Displaying Results:** The frontend UI component (`app/page.tsx`) receives the processed data from `/api/predictions` and renders the results (e.g., a list of findings) for the user to see.

This architecture keeps your ML API endpoint and token secure on the server-side (within the `/api/predictions` route) rather than exposing them directly in the browser.

## Using the Frontend

Once running, you can typically:

1.  Find the search input field on the page (`http://localhost:3000`).
2.  Type in your query related to the kind of information Project Fleming indexes (e.g., "how to implement authentication in python", "database connection pooling best practices", "find repository for UI components").
3.  Submit the query (e.g., by pressing Enter or clicking a search button).
4.  View the results displayed on the page, which are fetched from your configured Project Fleming ML API via the frontend's internal API.

## Customization

If you want to modify the frontend:

* **UI Changes:** Edit the React component file located at `app/page.tsx`. This is where the main page structure, input fields, and results display logic reside. The page will auto-update in your browser as you save changes when the development server is running.
* **Data Handling/Processing:** If you need to change how data from the ML API is processed *before* being shown in the UI, modify the internal API route handler (`app/api/predictions/route.ts` or a similar file depending on your specific setup).

## Troubleshooting

* **Error connecting to API / No results:**
    * Double-check the `ML_API` URL in your `.env` file. Is it correct and accessible? Is the path correct?
    * Verify the `API_AUTH_TOKEN` in your `.env` file. Is it valid?
    * Ensure the Project Fleming backend server is running and reachable from where you are running the frontend development server.
    * Check the console output in your terminal (where you ran `npm run dev`) and the browser's developer console (F12) for specific error messages. Errors might originate from the `/api/predictions` route or the Project Fleming backend itself.
* **Application doesn't start:**
    * Ensure all dependencies were installed correctly (`npm install` or equivalent).
    * Make sure you have a compatible version of Node.js installed.
    * Check if the `.env` file exists, even if you haven't filled it yet, as some setups might expect it.


## Advanced Settings

The application includes an Advanced Settings feature that allows users to override the default ML API configuration without modifying environment variables. This is particularly useful for:

- Testing against different ML API endpoints
- Using custom authentication tokens
- Development and debugging scenarios
- Multi-environment configurations

### Features

- **Custom API URL**: Override the default `ML_API` endpoint with a custom URL
- **Custom Auth Token**: Override the default `API_AUTH_TOKEN` with a custom authentication token
- **Persistent Storage**: Settings are saved in browser's localStorage and persist across sessions
- **Visual Indicators**: The Advanced Settings button shows a blue indicator when custom settings are active
- **Reset Functionality**: Easily reset to default environment variable values

### How to Use Advanced Settings

1. **Access**: Click the "Advanced" button in the search interface
2. **Configure**: Enter your custom API URL and/or authentication token in the dialog
3. **Save**: Click "Save Settings" to apply and persist your changes
4. **Reset**: Use "Reset to Default" to clear custom settings and return to environment variables

### Settings Priority

The application follows this priority order for configuration:

1. **Custom Settings** (highest priority) - Settings configured through the Advanced Settings dialog
2. **Environment Variables** (fallback) - Default settings from `.env` file

When custom settings are active, they completely override the corresponding environment variables for that session.

### Storage

- Custom settings are stored in the browser's localStorage
- Settings persist across browser sessions until manually reset
- Settings are scoped to the specific browser/device

## API

### `api/predictions`

This API endpoint is responsible for fetching an array of predictions from the machine learning model. It processes the data to ensure it is easy for the frontend to render.

To use this endpoint, make a GET request to `/api/predictions`. The response will include the processed predictions ready for display on the frontend.

The endpoint automatically uses either the environment variables or custom settings (if configured) for ML API communication.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!
