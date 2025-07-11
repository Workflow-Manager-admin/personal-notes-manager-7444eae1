#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks.

    This entrypoint is intended for Django development and admin commands.
    To run the Django server on a specific port such as 3001, you should use:

        python manage.py runserver 0.0.0.0:3001

    If you encounter issues where the server is not reachable on port 3001,
    ensure that:
        - There are no syntax errors in settings or code.
        - All dependencies are installed (see requirements.txt).
        - The host is set to '0.0.0.0' and port is 3001 on runserver call.

    For Docker or container environments, confirm that port 3001 is mapped.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
