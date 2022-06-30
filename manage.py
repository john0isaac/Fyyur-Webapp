from flask_script import Manager
from flask_migrate import MigrateCommand

from app import app, migrate
from models import db

manager = Manager(app)
db.init_app(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()