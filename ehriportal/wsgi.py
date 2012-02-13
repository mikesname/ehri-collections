import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

venv_path = os.path.abspath(os.path.join(PROJECT_ROOT, "../../../"))
activate_this = os.path.join(venv_path, "bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))


sys.stderr.write("WSGI Python Path: %s\n" % sys.path)

from django.core.handlers.wsgi import WSGIHandler

import pinax.env

# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)


# set application for WSGI processing
application = WSGIHandler()
