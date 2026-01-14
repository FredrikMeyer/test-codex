# Backend

## Project Structure

```
backend/
├── app/          # Application code
│   ├── __init__.py
│   └── main.py
└── tests/        # Test code
    ├── __init__.py
    └── test_login_flow.py
```

## Usage

- `uv run python -m app.main` - to run your Flask app
- `uv add <package>` - to add new dependencies
- `uv sync` - to sync dependencies from the lockfile

## Running Tests

Run all tests:
```bash
uv run pytest
```

Run tests with verbose output:
```bash
uv run pytest -v
```

Run a specific test file:
```bash
uv run pytest tests/test_login_flow.py
```

Run tests with coverage:
```bash
uv run pytest --cov=app
```
