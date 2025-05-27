This is a Next.js project bootstrapped with `create-next-app`.

This repository is a Generic UI for Project Flemming. It demonstrates an example use of the ML endpoint of Project Flemming.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open http://localhost:3000 with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Environment Variables

Create a `.env` file in the root of your project to store environment variables. Here are the variables you need:

```plaintext
ML_API=
API_AUTH_TOKEN=
```

- `ML_API`: The endpoint for your machine learning model's API.
- `API_AUTH_TOKEN`: The authentication token required to access the API.

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
