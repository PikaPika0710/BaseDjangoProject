#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()


# def create_database():
#     mydb = mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         port=os.getenv("DB_PORT")
#     )
#     mycursor = mydb.cursor()
#     mycursor.execute("SHOW DATABASES")
#     for x in mycursor:
#         if x[0] == os.getenv("DB_NAME"):
#             return
#     mycursor.execute("CREATE DATABASE " + os.getenv("DB_NAME"))
#

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
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
    # create_database()
    main()
