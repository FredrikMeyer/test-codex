import json
import os
import random
import string
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, request


def _default_data() -> Dict[str, Any]:
    return {"codes": [], "logs": []}


def _ensure_data_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(_default_data(), indent=2))


def _load_data(path: Path) -> Dict[str, Any]:
    _ensure_data_file(path)
    with path.open() as fp:
        return json.load(fp)


def _save_data(path: Path, data: Dict[str, Any]) -> None:
    _ensure_data_file(path)
    with path.open("w") as fp:
        json.dump(data, fp, indent=2)


def _generate_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=4))


def create_app(data_file: str | Path | None = None) -> Flask:
    app = Flask(__name__)
    app.config["DATA_FILE"] = Path(
        data_file or os.environ.get("ASTHMA_DATA_FILE") or "backend/data/storage.json"
    )
    data_lock = threading.Lock()

    def read_data() -> Dict[str, Any]:
        with data_lock:
            return _load_data(app.config["DATA_FILE"])

    def write_data(data: Dict[str, Any]) -> None:
        with data_lock:
            _save_data(app.config["DATA_FILE"], data)

    @app.post("/generate-code")
    def generate_code() -> Any:
        code = _generate_code()
        data = read_data()
        data["codes"].append(
            {"code": code, "created_at": datetime.utcnow().isoformat() + "Z"}
        )
        write_data(data)
        return jsonify({"code": code})

    @app.post("/login")
    def login() -> Any:
        payload = request.get_json(silent=True) or {}
        code = payload.get("code")
        if not code:
            return jsonify({"error": "Code is required"}), 400

        data = read_data()
        for entry in data.get("codes", []):
            if entry["code"] == code:
                entry["last_login_at"] = datetime.utcnow().isoformat() + "Z"
                write_data(data)
                return jsonify({"status": "ok"})

        return jsonify({"error": "Invalid code"}), 400

    @app.post("/logs")
    def save_log() -> Any:
        payload = request.get_json(silent=True) or {}
        code = payload.get("code")
        log = payload.get("log")

        if not code or not isinstance(log, dict):
            return (
                jsonify({"error": "Both 'code' and 'log' (object) are required"}),
                400,
            )

        data = read_data()
        matching_codes = {entry["code"] for entry in data.get("codes", [])}
        if code not in matching_codes:
            return jsonify({"error": "Unknown code"}), 400

        data["logs"].append(
            {
                "code": code,
                "log": log,
                "received_at": datetime.utcnow().isoformat() + "Z",
            }
        )
        write_data(data)
        return jsonify({"status": "saved"})

    return app


app = create_app()
