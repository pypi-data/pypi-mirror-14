# Copyright (C) 2014 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from heralding.misc.session import Session

logger = logging.getLogger(__name__)


class HandlerBase(object):
    def __init__(self, options):
        """
        Base class that all capabilities must inherit from.

        :param sessions: a dictionary of Session objects.
        :param options: a dictionary of configuration options.
        """
        self.options = options
        self.sessions = {}
        self.users = {}

        self.port = int(options['port'])

    def create_session(self, address):
        protocol = self.__class__.__name__.lower()
        session = Session(address[0], address[1], protocol, self.users)
        self.sessions[session.id] = session
        session.destination_port = self.port
        logger.debug(
            'Accepted {0} session on port {1} from {2}:{3}. ({4})'.format(protocol, self.port, address[0],
                                                                          address[1], str(session.id)))
        logger.debug('Size of session list for {0}: {1}'.format(protocol, len(self.sessions)))
        return session

    def close_session(self, session):
        logger.debug('Closing sessions')
        session.end_session()
        if session.id in self.sessions:
            del self.sessions[session.id]
        else:
            assert False

    def handle_session(self, socket, address):
        raise Exception('Do no call base class!')
