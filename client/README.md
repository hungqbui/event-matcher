### React Client Application
This is the client-side application for our project, built with React and Vite.

### Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
You need to have Node.js (version 18 or later is recommended) and npm installed on your machine. You can verify your installation by running:
```
node -v
npm -v
```
### Installation & Setup
Follow these steps to set up the development environment:

1. Clone the repository
```
git clone <your-repository-url>
cd <your-project-directory>
```
2. Install dependencies
```
npm install
```
3. Run the development server
This command starts the Vite development server, usually on http://localhost:5173. The application will automatically reload if you change any of the source files.
```
npm run dev
```

### Available Scripts
In the project directory, you can run:

```npm run dev```
Runs the app in development mode. Open http://localhost:5173 to view it in the browser.

```npm run build```
Builds the app for production to the dist folder. It correctly bundles React in production mode and optimizes the build for the best performance.

### Consistency Notes
- Create pages in ```src/pages```, reusable components in ```src/components```.
- If you want to define a custom hook or need reference to one, it's in ```src/hooks``` (e.g. auth context)
- Define fetch tools, utilities in ```src/utils``` (e.g. fetch event data)
- Use the theme variables defined globally in the theme.css file to keep the color palette consistent across the pages. (TODO)