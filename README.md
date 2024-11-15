## What's this?
A wee project for hosting weedgets
# Project Setup
### Frameworks
Flask for the backend.
### Frontend
A simple grid-based layout using HTML/CSS (e.g., Bootstrap or a custom CSS grid).
### Database
SQLite to store widget HTML as strings (or any other associated metadata).
### Deployment
GitHub Actions for CI/CD.

# API Design
### Routes:
- GET /widgets: Fetch a list of all widgets with their metadata and HTML previews.
- POST /widgets: Add a new widget (HTML content and metadata like name).
- GET /widgets/<id>: Fetch a specific widget's details.
- DELETE /widgets/<id>: Remove a widget.

# Widget Preview UI
### A simple grid layout
Each grid item shows a widget preview (rendered from the stored HTML string).
Slight gaps between widgets for a clean look.
Option to embed widgets in Notion via an iframe or similar embed code.

# Tech Stack
### Backend
Flask, SQLite.
### Frontend
Jinja2 templates for rendering previews in the UI.
### Hosting
GitHub Pages + GitHub Actions for API deployment.
### GitHub Actions for CI/CD
- CI:<br>
Run Python tests for API routes.
Linting with flake8 or black.
- CD:<br>
Push to a hosting platform like Heroku, AWS, or fly.io.