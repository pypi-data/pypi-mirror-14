# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Stuff
"""

from __future__ import unicode_literals

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None
else:
    from sqlalchemy import orm
    from sqlalchemy.orm.exc import NoResultFound

from rattail.config import ConfigExtension as BaseExtension


if sqlalchemy:

    class SessionBase(orm.Session):
        """
        Custom SQLAlchemy session class, which adds some convenience methods
        related to the SQLAlchemy-Continuum integration.
        """

        def __init__(self, continuum_user=None, **kwargs):
            """
            Custom constructor, to allow specifying the Continuum user at session
            creation.  If ``continuum_user`` is specified, its value will be passed
            to :meth:`set_continuum_user()`.
            """
            super(SessionBase, self).__init__(**kwargs)
            if continuum_user is None:
                self.continuum_user = None
            else:
                self.set_continuum_user(continuum_user)

        def set_continuum_user(self, user_info):
            """
            Set the effective Continuum user for the session.

            :param user_info: May be a :class:`model.User` instance, or the
              ``uuid`` or ``username`` for one.
            """
            from rattail.db import model

            if isinstance(user_info, model.User):
                user = user_info
            else:
                user = self.query(model.User).get(user_info)
                if not user:
                    try:
                        user = self.query(model.User).filter_by(username=user_info).one()
                    except NoResultFound:
                        user = None
            self.continuum_user = user


    Session = orm.sessionmaker(class_=SessionBase)

else: # no sqlalchemy
    Session = None


class ConfigExtension(BaseExtension):
    """
    Config extension for the ``rattail.db`` subpackage.  This extension is
    responsible for loading the available Rattail database engine(s), and
    configuring the :class:`Session` class with the default engine.  This
    extension expects to find something like the following in your config file:

    .. code-block:: ini

       [rattail.db]
       keys = default, host, other
       default.url = postgresql://localhost/rattail
       host.url = postgresql://host-server/rattail
       other.url = postgresql://other-server/rattail

    The result of this extension's processing is that the config object will
    get two new attributes:

    .. attribute:: rattail.config.RattailConfig.rattail_engines

       Dict of available Rattail database engines.  Keys of the dict are the
       same as found in the config file; values are the database engines.  Note
       that it is possible for this to be an empty dict.

    .. attribute:: rattail.config.RattailConfig.rattail_engine

       Default database engine; same as ``rattail_engines['default']``.  Note
       that it is possible for this value to be ``None``.
    """
    key = 'rattail.db'

    def configure(self, config):
        from rattail.db.config import get_engines, configure_session, configure_versioning

        if Session:
            config.rattail_engines = get_engines(config)
            config.rattail_engine = config.rattail_engines.get('default')
            Session.configure(bind=config.rattail_engine)
            configure_session(config, Session)
            if config.getbool('rattail.db', 'versioning.enabled', default=False):
                configure_versioning(config)
