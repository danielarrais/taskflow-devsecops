from app_instrumented import app, init_db

bind = "0.0.0.0:5000"
workers = 2
accesslog = None
errorlog = "-"


def on_starting(server):
    with app.app_context():
        init_db()
