"""
Flask Entrypoint
"""

import os

import click
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from runner import create_app, db

app = create_app(os.getenv("FLASK_CONFIG", "development"))


FlaskInjector(app=app, modules=[])
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {
        "app": app,
        "db": db,
    }  # Add any additional objects you want to access in the shell


def print_env_variables():
    """Prints all the env variables"""
    print("Printing ENV Variables")
    for key, value in os.environ.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run()
