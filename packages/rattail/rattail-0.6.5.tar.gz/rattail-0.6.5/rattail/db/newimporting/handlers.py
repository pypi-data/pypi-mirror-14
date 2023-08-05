# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
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
Import Handlers
"""

from __future__ import unicode_literals, absolute_import

import sys
import logging

from rattail.util import OrderedDict
from rattail.mail import send_email
from rattail.db.importing import RecordRenderer


log = logging.getLogger(__name__)


class ImportHandler(object):
    """
    Base class for all import handlers.
    """
    local_title = "Rattail"
    host_title = "Host/Other"
    session = None
    progress = None

    def __init__(self, config=None, **kwargs):
        self.config = config
        self.importers = self.get_importers()
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_importers(self):
        """
        Returns a dict of all available importers, where the values are
        importer factories.  All subclasses will want to override this.  Note
        that if you return an ``OrderedDict`` instance, you can affect the
        ordering of keys in the command line help system, etc.
        """
        return {}

    def get_importer_keys(self):
        """
        Returns a list of keys corresponding to the available importers.
        """
        return list(self.importers.iterkeys())

    def get_default_keys(self):
        """
        Returns a list of keys corresponding to the default importers.
        Override this if you wish certain importers to be excluded by default,
        e.g. when first testing them out etc.
        """
        return self.get_importer_keys()

    def get_importer(self, key):
        """
        Returns an importer instance corresponding to the given key.
        """
        kwargs = self.get_importer_kwargs(key)
        kwargs['config'] = self.config
        kwargs['session'] = self.session
        return self.importers[key](**kwargs)

    def get_importer_kwargs(self, key):
        """
        Return a dict of kwargs to be used when construcing an importer with
        the given key.
        """
        return {}

    def import_data(self, keys, args):
        """
        Import all data for the given importer keys.
        """
        self.setup()
        changes = OrderedDict()

        for key in keys:
            importer = self.get_importer(key)
            if not importer:
                log.warning("skipping unknown importer: {}".format(key))
                continue

            created, updated, deleted = importer.import_data(args, progress=self.progress)

            changed = bool(created or updated or deleted)
            logger = log.warning if changed and args.warnings else log.info
            logger("{} -> {}: added {}, updated {}, deleted {} {} records".format(
                self.host_title, self.local_title, len(created), len(updated), len(deleted), key))
            if changed:
                changes[key] = created, updated, deleted

        if changes:
            self.process_changes(changes, args)

        self.teardown()
        return changes

    def setup(self):
        """
        Perform any setup necessary, prior to running the import task(s).
        """

    def teardown(self):
        """
        Perform any cleanup necessary, after running the import task(s).
        """

    def process_changes(self, changes, args):
        """
        This method is called any time changes occur, regardless of whether the
        import is running in "warnings" mode.  Default implementation however
        is to do nothing unless warnings mode is in effect, in which case an
        email notification will be sent.
        """
        # TODO: This whole thing needs a re-write...but for now, waiting until
        # the old importer has really gone away, so we can share its email
        # template instead of bothering with something more complicated.

        if not args.warnings:
            return

        data = {
            'local_title': self.local_title,
            'host_title': self.host_title,
            'argv': sys.argv,
            'updates': changes,
            'dry_run': args.dry_run,
            'render_record': RecordRenderer(self.config),
        }

        command = getattr(self, 'command', None)
        if command:
            data['command'] = '{} {}'.format(command.parent.name, command.name)
        else:
            data['command'] = None

        if command:
            key = '{}_{}_updates'.format(command.parent.name, command.name)
            key = key.replace('-', '_')
        else:
            key = 'rattail_import_updates'

        send_email(self.config, key, fallback_key='rattail_import_updates', data=data)


class SQLAlchemyImportHandler(ImportHandler):
    """
    Handler for imports for which the external data source is represented by a
    SQLAlchemy engine and ORM.
    """

    def make_host_session(self):
        raise NotImplementedError

    def setup(self):
        self.host_session = self.make_host_session()

    def teardown(self):
        self.host_session.close()

    def get_importer_kwargs(self, key):
        return {'host_session': self.host_session}
