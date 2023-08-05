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
Data Models
"""

from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from rattail.core import Object

# These are imported because most sibling modules import them *from* here (if
# that makes sense).  Probably need to think harder about the "best" place for
# these things to live.
from rattail.db.core import uuid_column, getset_factory
from rattail.db.types import GPCType


class ModelBase(Object):
    """
    Base class for all data models.
    """

    def __repr__(self):
        mapper = orm.object_mapper(self)
        keys = ['{0}={1}'.format(k.key, repr(getattr(self, k.key))) for k in mapper.primary_key]
        return "{0}({1})".format(self.__class__.__name__, ', '.join(keys))


Base = declarative_base(cls=ModelBase)


class Setting(Base):
    """
    Represents a setting stored within the database.
    """

    __tablename__ = 'setting'

    name = sa.Column(sa.String(length=255), primary_key=True)
    value = sa.Column(sa.Text())

    def __unicode__(self):
        return unicode(self.name or '')


class Change(Base):
    """
    Represents a changed (or deleted) record, which is pending synchronization
    to another database.
    """
    __tablename__ = 'change'

    uuid = uuid_column()

    class_name = sa.Column(sa.String(length=40), nullable=False)
    instance_uuid = sa.Column(sa.String(length=32), nullable=False)
    deleted = sa.Column(sa.Boolean(), nullable=False)

    def __repr__(self):
        return "Change(class_name={}, instance_uuid={}, deleted={})".format(
            repr(self.class_name), repr(self.instance_uuid), repr(self.deleted))
