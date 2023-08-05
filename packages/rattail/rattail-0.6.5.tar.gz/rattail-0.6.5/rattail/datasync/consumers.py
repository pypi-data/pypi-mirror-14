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
DataSync Consumers
"""

from __future__ import unicode_literals
from __future__ import absolute_import

from rattail.config import parse_list


class DataSyncConsumer(object):

    def __init__(self, config, key, dbkey=None):
        self.config = config
        self.key = key
        self.dbkey = dbkey

    def process_changes(self, session, changes):
        """
        Process (consume) a set of changes.
        """


class ErrorTestConsumer(DataSyncConsumer):
    """
    Consumer which always raises an error when processing changes.  Useful for
    testing error handling etc.
    """

    def process_changes(self, session, changes):
        raise RuntimeError("Fake exception, to test error handling")
