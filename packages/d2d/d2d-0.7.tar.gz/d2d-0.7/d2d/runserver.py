import os
import sys
import socket
from django.core.management import execute_from_command_line

#----------------------------------------------------------------------
def runserver(settings):
    """"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((settings.get("IP"), int(settings.get("PORT"))))

    if result == 0:
        print("App is running")
    else:
        sys.path.append(settings.get("APPNAME"))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings"%settings.get("APPNAME"))
        execute_from_command_line([os.path.join(os.path.split(sys.argv[0])[0], settings.get("APPNAME"), "manage.py"), "runserver", settings.get("PORT"), "--noreload"])
