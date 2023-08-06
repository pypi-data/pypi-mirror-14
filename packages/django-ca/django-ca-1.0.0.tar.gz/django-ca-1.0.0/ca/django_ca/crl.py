# -*- coding: utf-8 -*-
#
# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca.  If not,
# see <http://www.gnu.org/licenses/>.

from OpenSSL import crypto

from django.utils import timezone

from django_ca.models import Certificate


def get_crl(ca, **kwargs):
    """Function to generate a Certificate Revocation List (CRL).

    All keyword arguments are passed as-is to :py:func:`OpenSSL.crypto.CRL.export`. Please see the
    documentation of that function for details.

    Parameters
    ----------

    type : int
    days : int
    digest : hash
        Unlike the current pyOpenSSL default (md5), sha512 is the default.


    Returns
    -------

    Returns the CRL as bytes (since this is what pyOpenSSL returns).
    """
    kwargs.setdefault('digest', b'sha512')

    crl = crypto.CRL()
    for cert in Certificate.objects.filter(ca=ca, expires__gt=timezone.now()).revoked():
        crl.add_revoked(cert.get_revocation())
    return crl.export(ca.x509, ca.key, **kwargs)
