"""TaskFlow instrumentada com logs JSON seguros para Loki."""

import hmac
import json
import logging
import os
import secrets
import sqlite3
import uuid
from datetime import UTC, datetime

from flask import Flask, abort, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

SEED_USERS = (("admin", "TASKFLOW_ADMIN_PASSWORD"), ("aluno", "TASKFLOW_ALUNO_PASSWORD"))
RESERVED_LOG_FIELDS = {"password", "token", "cookie", "authorization", "secret"}


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Variavel de ambiente {name} nao foi definida.")
    return value


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        fields = getattr(record, "event_fields", {})
        payload.update(
            {key: value for key, value in fields.items() if key.lower() not in RESERVED_LOG_FIELDS}
        )
        return json.dumps(payload, ensure_ascii=True)


def configure_logger():
    logger = logging.getLogger("taskflow")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = JsonFormatter()

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    log_file = os.environ.get("TASKFLOW_LOG_FILE")
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


logger = configure_logger()
app = Flask(__name__)
app.config["SECRET_KEY"] = require_env("TASKFLOW_SECRET_KEY")
app.config["DATABASE"] = os.environ.get("TASKFLOW_DATABASE", "taskflow.db")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("TASKFLOW_COOKIE_SECURE", "0") == "1"


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def validate_csrf():
    submitted = request.form.get("csrf_token", "")
    if not hmac.compare_digest(submitted, session.get("csrf_token", "")):
        abort(400)


app.jinja_env.globals["csrf_token"] = csrf_token


def log_event(event, **fields):
    fields.update(event=event, request_id=getattr(g, "request_id", None))
    logger.info(event, extra={"event_fields": fields})


@app.before_request
def assign_request_id():
    g.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())


@app.after_request
def log_response(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; script-src 'self'; style-src 'self'; "
        "img-src 'self'; font-src 'self'; connect-src 'self'; frame-src 'none'; "
        "frame-ancestors 'none'; form-action 'self'; base-uri 'none'; object-src 'none'; "
        "manifest-src 'self'; media-src 'self'; worker-src 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), geolocation=(), microphone=()"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Request-ID"] = g.request_id
    log_event(
        "http_response",
        method=request.method,
        path=request.path,
        status=response.status_code,
        remote_addr=request.remote_addr,
    )
    return response


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            done INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    if db.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"] == 0:
        for username, password_env in SEED_USERS:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(require_env(password_env))),
            )
    db.commit()


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


@app.route("/")
def index():
    return redirect(url_for("tasks" if "user_id" in session else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        validate_csrf()
        username = request.form["username"]
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password"], request.form["password"]):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            log_event("login_succeeded", username=username, remote_addr=request.remote_addr)
            return redirect(url_for("tasks"))
        # Nunca registrar request.form: ele contém a senha.
        log_event("login_failed", username=username, remote_addr=request.remote_addr)
        error = "Usuario ou senha invalidos."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/tasks")
def tasks():
    if "user_id" not in session:
        return redirect(url_for("login"))
    search = request.args.get("q", "")
    db = get_db()
    if search:
        rows = db.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND title LIKE ?",
            (session["user_id"], f"%{search}%"),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM tasks WHERE user_id = ?", (session["user_id"],)).fetchall()
    log_event(
        "tasks_list", user_id=session["user_id"], result_count=len(rows), search_used=bool(search)
    )
    return render_template("tasks.html", username=session["username"], search=search, tasks=rows)


@app.route("/tasks/new", methods=["GET", "POST"])
def new_task():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        validate_csrf()
        title = request.form["title"]
        db = get_db()
        db.execute(
            "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
            (session["user_id"], title, request.form["description"]),
        )
        db.commit()
        log_event("task_created", user_id=session["user_id"], title_length=len(title))
        return redirect(url_for("tasks"))
    return render_template("new_task.html")


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
