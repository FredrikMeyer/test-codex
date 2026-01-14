# Frontend

Offline-friendly web application for tracking daily asthma medication usage.

## Files

- `index.html` - Main application page
- `app.js` - Application logic (counter, storage, CSV export)
- `styles.css` - Application styles
- `service-worker.js` - Offline support
- `manifest.webmanifest` - PWA configuration

## Features

- Track daily medication doses with a simple counter interface
- Store data locally in browser localStorage
- Works offline via service worker
- Export usage history as CSV
- Progressive Web App (installable on mobile devices)

## Development

Open `index.html` in a browser. For service worker to function, serve via HTTP:

```bash
python -m http.server 8000
```

Then visit http://localhost:8000/

## Deployment

The frontend is deployed to GitHub Pages at `/codex/` via the `pages.yml` workflow.
