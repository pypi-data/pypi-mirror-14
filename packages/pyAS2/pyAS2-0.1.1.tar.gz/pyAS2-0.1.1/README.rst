=====
pyAS2
=====

pyAS2 is a python implementation of the AS2 file transfer protocol.
The application conforms to the AS2 1.2 specifications as per the RFC 4130.
This Django based app acts as both client and server i.e. it enables both
sending/receiving of files.

Quick start
-----------

1. Add "pyas2" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'pyas2',
    )

2. Include the pyAS2 URLconf in your project urls.py like this::

    url(r'^pyas2/', include('pyas2.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. If you are using cherrypy, start the server and with the command 
   `python manage.py runas2server` and visit http://127.0.0.1:8080/pyas2/
   to configure the app and start sending/receiving files.

