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
Application
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
import gevent

standard_library.install_aliases()
from builtins import *
from builtins import str
from builtins import object
import logging
from gevent import pool
import signal

#: Application name
Name = 'mailfilter'
#: Signal names
Signals = {v: k for k, v in list(signal.__dict__.items()) if k.startswith('SIG') and isinstance(v, int)}

DEFAULT_FOLDERS = ['INBOX']

class Application(object):
    """
    Application
    """
    def __init__(self):
        self.folders = []
        self.config = None
        self.greenletPool = None
        self.log = logging.getLogger('{}.{}.{}'.format(Name, str(self.__module__), __name__))
        self.log.info('created')

    def init(self, config):
        """
        Create Application

        :param config: configuration
        :type config: dict
        """
        self.log.info('init ==============================================================')
        self.config = config
        signal.signal(signal.SIGINT, Stop)
        signal.signal(signal.SIGTERM, Stop)
        signal.signal(signal.SIGQUIT, Stop)

    def run(self):
        """
        Run application

        """
        from .folder import Folder

        self.log.info('run')
        self.greenletPool = pool.Pool()
        for name, config in list(self.config('accounts').items()):
            if config.get('enabled', True):
                af = Folder(name, config.folders, config, self.config('global', default={}))
                self.folders.append(af)
                self.greenletPool.spawn(af.run)
            else:
                self.log.info('%s disabled', name)
        self.greenletPool.join()

    def stop(self):
        self.greenletPool.kill(block=False)

    def terminate(self):
        """
        Terminate application

        """
        self.log.info('Terminating')

def Stop(signo, frame):
    """
    Stop application

    :param signo: signal number
    :type signo: int
    :param frame:
    """
    log = logging.getLogger('{}.{}'.format(Name, __name__))
    log.info('Got %s', Signals[signo])
    App.stop()

App = Application()
