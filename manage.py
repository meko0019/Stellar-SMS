import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

base_dir = os.path.dirname(os.path.abspath(__file__))


def main():
    command = sys.argv[1]
    if command == "db":

        from client.database import db
        from client.factory import create_app

        app = create_app()
        manager = Manager(app)

        Migrate(
            app,
            db,
            directory=os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "client",
                "database",
                "migrations",
            ),
        )
        manager.add_command("db", MigrateCommand)
        return manager.run()

    else:

        if command == "shell":
            return system("docker-compose build web && docker-compose run --rm web sh")

        if command == "up":
            return system("docker-compose build web && docker-compose up")

        if command == "initdb":
            return system(
                "docker-compose build web "
                "&& docker-compose run web python manage.py db upgrade"
            )

        if command == "psql":
            return system("psql -h postgres -U postgres -w postgres")


def system(command):
    print(f"+ {command}")
    return os.system(command)


if __name__ == "__main__":
    sys.exit(main())
