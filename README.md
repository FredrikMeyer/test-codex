# Asthma Medicine Tracker

Offline-friendly web app for logging daily asthma medication usage and exporting a CSV history.

## Usage
- Open `index.html` (or deploy the contents of this folder) at `/codex/`.
- Pick a date, adjust the counter with the plus/minus buttons, and **Save count**.
- Use **Reset day** to clear a date and **Export CSV** to download your history.

Data is stored locally in the browser and works offline via the included service worker.

## Backend (prototype)
A simple Flask backend is available for generating login codes, performing login, and accepting asthma log entries.

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the server
```bash
FLASK_APP=backend.app flask run
```

### Endpoints
- `POST /generate-code` → returns a new 4-character code.
- `POST /login` → body `{"code": "<CODE>"}` validates a generated code.
- `POST /logs` → body `{"code": "<CODE>", "log": {<your data>}}` stores an asthma log entry in `backend/data/storage.json`.
