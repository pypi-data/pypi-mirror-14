#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jfernandez@bioiberica.com>

PyramidPlugin offers way of integrating Pyramid framework with
SQLAlchemy-Continuum. Pyramid-Plugin adds two columns for Transaction model,
namely `user_id` and `remote_addr`.

These columns are automatically populated when transaction object is created.
The `remote_addr` column is populated with the value of the remote address that
made current request. The `user_id` column is populated with the id of the
current_user object.

::

    from pyramid_sqlalchemy_continuum import PyramidPlugin
    from sqlalchemy_continuum import make_versioned


    make_versioned(plugins=[PyramidPlugin()])
"""
from __future__ import absolute_import

pyramid = None
try:
    import pyramid
    from pyramid.security import authenticated_userid
    from pyramid.threadlocal import get_current_request
except ImportError:
    pass
from sqlalchemy_utils import ImproperlyConfigured
from sqlalchemy_continuum.plugins import Plugin


def fetch_current_user_id():
    request = get_current_request()

    # Return None if we are outside of request context.
    if request is None:
        return
    return authenticated_userid(request)


def fetch_remote_addr():
    request = get_current_request()

    # Return None if we are outside of request context.
    if request is None:
        return
    return request.client_addr


class PyramidPlugin(Plugin):

    def __init__(
        self,
        current_user_id_factory=None,
        remote_addr_factory=None
    ):
        self.current_user_id_factory = (
            fetch_current_user_id if current_user_id_factory is None
            else current_user_id_factory
        )
        self.remote_addr_factory = (
            fetch_remote_addr if remote_addr_factory is None
            else remote_addr_factory
        )

        if not pyramid:
            raise ImproperlyConfigured(
                'Pyramid is required with PyramidPlugin. Please install Pyramid by'
                ' running pip install Pyramid'
            )

    def transaction_args(self, uow, session):
        return {
            'user_id': self.current_user_id_factory(),
            'remote_addr': self.remote_addr_factory()
        }

