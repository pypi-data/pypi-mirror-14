django-ca is a small project to manage TLS certificate authorities and easily
issue certificates. It is based on `pyOpenSSL <https://pyopenssl.readthedocs.org/>`_ and `Django
<https://www.djangoproject.com/>`_. It can be used as an app in an existing Django project or
stand-alone with the basic project included. Certificates can be managed through Djangos admin
interface or via manage.py commands - so no webserver is needed, if you’re happy with the
command-line.

Features:

* Set up a secure local certificate authority in just a few minutes.
* Written in Python 2.7/Python3.4+.
* Manage your entire certificate authority from the command line and/or via Djangos admin interface.
* Get email notifications about certificates about to expire.
* Support generating for certificate revocation lists (CRLs).
* Generates index files that can be used with the openssl ocsp command for a crude OCSP service.

Please see https://django-ca.readthedocs.org for more extensive documentation.


