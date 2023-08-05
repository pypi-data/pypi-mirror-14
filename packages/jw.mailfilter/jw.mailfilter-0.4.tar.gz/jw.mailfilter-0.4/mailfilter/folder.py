# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Account
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from pprint import pprint
from future import standard_library
standard_library.install_aliases()
from itertools import takewhile, chain
import email

from builtins import str
from builtins import object
import gevent
from . import filters
from . import imap

import logging
from jw.util.extension import LoadClass
from . import app
import ssl
from .util import Flatten, D

#: Default IDLE timeout
IDLE_TIMEOUT = 180

class UndefinedFilter(RuntimeError):
    def __init__(self, error):
        RuntimeError.__init__(self, 'Undefined filter type: ' + error)

class Folder(object):

    def __init__(self, name, folders, config, globalConfig=None):
        """

        :param name: Mail filter name from config
        :type name: str
        :param config: config
        :type config: dict
        """
        assert isinstance(folders, list), 'folders must be a list'
        # Parameters
        self.name = name
        self.config = config
        self.globalConfig = globalConfig or {}
        self.timeout = config.get('time-out', globalConfig.get('time-out'))
        # Logging
        self.log = logging.getLogger('{}.{}'.format(app.Name, str(self.__module__), __name__))
        # Miscellaneous setup
        self.imap = None
        self.seen = set()
        if not self._startImap():
            raise RuntimeError('Account %s not startable' % (self.name))
        # Setup folders and filters
        self.folders = [
            (name, tuple(self._filterFromString(f) for f in Flatten(filters))) for name, filters in folders
        ]
        if any(filter.needsBody for filter in chain.from_iterable(f[1] for f in self.folders)):
            # Full body required
            self.fetchPart = self.messagePart = 'RFC822'
        else:
            # Only headers required
            self.fetchPart = 'BODY.PEEK[HEADER]'
            self.messagePart = 'BODY[HEADER]'
        self.log.info(
            'Account %s, folders %s: %s (%s)',
            self.name,
            ', '.join(str(f) for f in self.folders),
            self.config['address'],
            ('No SSL', 'SSL')[self.config.get('ssl', False)]
        )

    def run(self):
        """
        Mail filter

        """
        self.separator = self.imap.namespace()[0][0][1]
        idleOk = 'IDLE' in self.imap.capabilities()
        idleUsed = self.config.get('idle', idleOk)
        if idleUsed and idleUsed != idleOk:
            raise RuntimeError('Server does not support IDLE: ' + self.name)
        self._check('ALL')
        if idleUsed:
            self.imap.idle()
        while True:
            if idleUsed:
                idleResult = self.imap.idle_check(self.timeout)
                if idleResult and idleResult[1]:
                    self.log.debug('%s: %s', self.name, idleResult)
                    if idleUsed:
                        self.imap.idle_done()
                    self._check()
                    if idleUsed:
                        self.imap.idle()
            else:
                gevent.sleep(self.timeout or IDLE_TIMEOUT)
                self._check()
        self.log.critical('%s stopped', self.name)
        self.imap = None

    def _check(self, search='UNSEEN'):
        """
        Check messages
        """
        # Check all folders in account
        for folder, filters in self.folders:
            self.log.debug('Checking folder %s in %s', folder, self.name)
            # Try to select folder
            try:
                self.imap('select_folder', folder.replace('/', self.separator))
            except Exception as e:
                self.log.critical('From self.imap.select_folder("%s"): %s', folder, e)
                continue
            # Determine messages to scan
            idlist = set(self.imap('search', search))
            diff = idlist ^ self.seen
            todo = idlist - self.seen
            self.log.debug('To do: %s', todo)
            if not todo:
                continue
            mlist = self.imap('fetch', todo, self.fetchPart)
            self.seen ^= diff
            # Scan messages
            for m, msg in list(mlist.items()):
                self.log.debug('Checking message %s', m)
                # Get message from IMAP
                try:
                    message = email.message_from_string(msg[self.messagePart])
                except KeyError as e:
                    self.log.critical('%s part not found in message %s:\n%s', self.messagePart, msg, e)
                    continue
                subject = message['Subject']
                # Do checks until one of them returns True (stop action)
                # [Checks also trigger the actions]
                checks = list(
                    takewhile(
                        lambda item: item[1] != 'stop',
                        ((filter.filterDef['filter'], filter.check(m, self, message)) for filter in filters)
                    )
                )
                result = all(c[1] for c in checks)
                self.log.info('%s %s(%s): %s %s %s', m, self.name, folder, repr(subject), result, checks)
                # Add processed message
                self.seen.add(m)
            self.imap.expunge()

    def _startImap(self):
        # If connection exists, shut it down
        if self.imap is not None:
            try:
                self.imap.shutdown()
            except Exception as e:
                self.log.critical('From self.imap.shutdown() in %s: %s', self.name, e)
        # Set up SSL context
        context = ssl.create_default_context()
        context.check_hostname = False  # TODO: make configurable
        context.verify_mode = ssl.CERT_NONE  # TODO: make configurable
        # Create connection
        self.imap = imap.IMAP(
            self.config['address'], self.config['username'], self.config['password'],
            ssl=self.config.get('ssl', False), ssl_context=context
        )
        self.log.debug('Capabilites: %s', self.imap.capabilities())
        # Try to do STARTTLS
        if self.config.get('starttls', False):
            self.log.info('STARTTLS')
            try:
                self.imap._command_and_check('STARTTLS')
            except:
                self.log.exception('From STARTTLS command:')
        # self.imap.login(self.config['username'], self.config['password'])
        return True

    def _filterFromString(self, filterDef):
        """
        Create a Filter object from a definition

        :param filterDef:
        :type filterDef: dict
        :return: filter object
        :rtype: filters.Filter
        :raise filter.FilterError: if filter name is undefined
        """
        try:
            filterClass = LoadClass('jw.mailfilter.filter', filterDef['filter'], type_=filters.Filter)
        except KeyError:
            raise UndefinedFilter(str(filterDef))
        except Exception as e:
            print(dir(filters))
            raise filters.FilterError('Account definition error %s: %s' % (repr(e), repr(filterDef)))
        return filterClass(self.imap, filterDef, self.globalConfig)
