"""Task Manager API

A small Flask REST API for managing tasks. Built as a demo project to
practice CI/CD: automated testing, linting, and a GitHub Actions pipeline.
"""

from flask import Flask


def create_app():
    """Application factory so tests can spin up isolated app instances."""
    app = Flask(__name__)
    app.config["TASKS"] = {}
    app.config["NEXT_ID"] = 1

    from .routes import bp as tasks_bp

    app.register_blueprint(tasks_bp)

    return app
