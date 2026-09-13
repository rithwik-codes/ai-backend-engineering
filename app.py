import os
import logging

from dotenv import load_dotenv

# Load environment variables before application imports
load_dotenv()

from flask import Flask
from routes.greet_routes import greet_bp
from routes.career_routes import career_bp
from database import init_db


def create_app():

    app = Flask(__name__)

    log_level = os.getenv("LOG_LEVEL", "INFO")
    env_mode = os.getenv(
        "APP_ENV",
        "development"
    ).lower()

    # Terminal logging
    logging.basicConfig(
        level=getattr(
            logging,
            log_level.upper(),
            logging.INFO
        ),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info(
        f"Application started in {env_mode} mode"
    )

    app.config["DEBUG"] = (
        env_mode != "production"
    )

    # Initialize database
    init_db()

    # Register application routes
    app.register_blueprint(greet_bp)
    app.register_blueprint(career_bp)

    return app


app = create_app()


if __name__ == "__main__":

    print("Starting Flask server...")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )