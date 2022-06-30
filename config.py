import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Connect to the database
DB_USERNAME="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT=5432
DATABASE_NAME="fyyur"

# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DATABASE_NAME)

# For Production
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')