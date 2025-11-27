# Codeius GUI

The frontend React application for the Codeius AI Coding Agent.

## Development

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Setup
1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will start on `http://localhost:3000` and will automatically proxy API requests to the backend server.

### Environment Variables
Create a `.env` file in the root of the `Codeius-GUI` directory:

```
VITE_API_URL=/api
```

## Building for Production
To create a production build of the React app:

```bash
npm run build
```

This will create optimized build files in the `dist` directory.

## Features
- Real-time chat with the Codeius AI agent
- Multiple AI model selection
- Conversation history
- Responsive design for desktop and mobile
- Syntax highlighting for code
- Suggested prompts for quick start
- Settings panel for customization

## Architecture
- React 19 with hooks
- Vite as the build tool
- Tailwind CSS for styling (via custom CSS)
- Proxy configuration for development