# Project Flemming: Generic UI

This repository contains a generic user interface for Project Flemming, showcasing an example use of the discovery tool endpoint.

This is a Next.js project bootstrapped with `create-next-app`.

## Installing Next.js

### Windows

1. **Install Node.js**:
   - Download and install Node.js from nodejs.org.
   - Verify the installation by running `node -v` and `npm -v` in your command prompt.

2. **Create a Next.js Project**:
   - Open your command prompt and navigate to the directory where you want to create your project.
   - Run the following command to create a new Next.js app:
     ```bash
     npx create-next-app@latest my-next-app
     ```
   - Follow the prompts to set up your project.

3. **Navigate to Your Project Directory**:
   ```bash
   cd my-next-app
   ```

4. **Start the Development Server**:
   ```bash
   npm run dev
   ```
   - Open [http://localhost:3000](http://localhost:3000) in your browser to see your Next.js app.

### macOS

1. **Install Node.js**:
   - Download and install Node.js from nodejs.org.
   - Verify the installation by running `node -v` and `npm -v` in your terminal.

2. **Create a Next.js Project**:
   - Open your terminal and navigate to the directory where you want to create your project.
   - Run the following command to create a new Next.js app:
     ```bash
     npx create-next-app@latest my-next-app
     ```
   - Follow the prompts to set up your project.

3. **Navigate to Your Project Directory**:
   ```bash
   cd my-next-app
   ```

4. **Start the Development Server**:
   ```bash
   npm run dev
   ```
   - Open [http://localhost:3000](http://localhost:3000) in your browser to see your Next.js app.


## Getting Started

To start the development server, run one of the following commands:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open http://localhost:3000 in your browser to view the result.

You can begin editing the page by modifying `app/page.tsx`. The page will automatically update as you make changes.

## Environment Variables

Create a `.env` file in the root of your project to store environment variables. The required variables are:

```plaintext
ML_API=
API_AUTH_TOKEN=
```

- `ML_API`: The endpoint for your machine learning model's API.
- `API_AUTH_TOKEN`: The authentication token required to access the API.

## API

### `api/predictions`

This endpoint fetches an array of predictions from the machine learning model and processes the data for easy rendering on the frontend.

To use this endpoint, make a GET request to `/api/predictions`. The response will include the processed predictions ready for display.

## Learn More

For more information about Next.js, refer to the following resources:

- Next.js Documentation - Learn about Next.js features and API.
- Learn Next.js - An interactive Next.js tutorial.

You can also visit the Next.js GitHub repository to provide feedback and contributions.

