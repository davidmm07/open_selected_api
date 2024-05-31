import os
import logging
from flask_migrate import upgrade, stamp, migrate

# Ensure the environment variable is set
os.environ['FLASK_APP'] = './app/api.py'
os.environ['FLASK_ENV'] = 'Stg'  # or whatever your environment is

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your Flask app
from app.api import app

def run_migrations(event, context):
    logger.info("Starting migrations")
    with app.app_context():
        try:
            logger.info("Stamping the database with the current head")
            stamp(revision='head')
            logger.info("Generating new migration script")
            migrate()
            logger.info("Applying migrations")
            upgrade()
            logger.info("Migrations applied successfully")
        except Exception as e:
            logger.error(f"An error occurred during migrations: {e}")
            raise

if __name__ == "__main__":
    run_migrations()
