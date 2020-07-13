import os
import sys

if __name__ == "__main__":
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        pass
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

    # Override default port for 'runserver' command
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        if os.environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.production':
            from django.core.management.commands.runserver import Command as runserver
            runserver.default_port = "80"

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
