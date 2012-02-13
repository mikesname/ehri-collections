import sys
sys.path.insert(0, "/home/michaelb/ehri-collections/lib/python2.6/site-packages")

from django.core.handlers.wsgi import WSGIHandler

import pinax.env

# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)


# set application for WSGI processing
application = WSGIHandler()
