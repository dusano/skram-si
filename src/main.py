import os, sys, logging
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from appengine_django import InstallAppengineHelperForDjango
from appengine_django import have_django_zip
from appengine_django import django_zip_path
InstallAppengineHelperForDjango()

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Import the part of Django that we use here.
import django.core.handlers.wsgi


def main():  
    # Ensure the Django zipfile is in the path if required.
    if have_django_zip and django_zip_path not in sys.path:
        sys.path.insert(1, django_zip_path)
        logging.info('django path')
    
    # Adding lib folder to path
    LIB_PATH = 'lib'
    if LIB_PATH not in sys.path:
        sys.path.append(LIB_PATH)
    
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()

    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()