#
# Guidcheck Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2011 Mark Weirath (xlr8or@xlr8or.com)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA    02110-1301    USA
#
# Changelog:
#

__version__ = '0.1'
__author__  = 'xlr8or'

import re
import time
import b3
import b3.events

#--------------------------------------------------------------------------------------------------
class GuidcheckPlugin(b3.plugin.Plugin):
    requiresConfigFile = False
    _adminPlugin = None
    _guidregexp = ''
    _kickmessage = 'Invalid Guid'
    _strictlength = True

    def startup(self):
        """\
        Initialize plugin settings
        """
        # get the admin plugin so we can register commands
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            # something is wrong, can't start without admin plugin
            self.error('Could not find admin plugin')
            return False

        # Register our events
        self.verbose('Registering events')
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)

        # Define the proper regexp for our game version
        self._guidregexp = self.defineRegexp()

        if self.console.PunkBuster:
            self.disable()
            self.debug('PunkBuster is enabled, plugin disabled.')
        else:
            if self._strictlength:
                self.debug('Using strict length guid checking')
            else:
                self.debug('Using not so strict length guid checking')
            self.debug('Started')

    def onLoadConfig(self):
        pass

    def onEvent(self, event):
        """
        Handle intercepted events
        """
        if not self.isEnabled:
            return None

        if (event.type == b3.events.EVT_CLIENT_AUTH):
            self.checkGuid(event.client)
        else:
            self.dumpEvent(event)

    def dumpEvent(self, event):
        """
        dumpEvent shows us the registered, yet unused or unhandled events.
        """
        self.debug('guidcheck.dumpEvent -- Type %s, Client %s, Target %s, Data %s',
                   event.type, event.client, event.target, event.data)

    def checkGuid(self, client):
        if not re.match(self._guidregexp, client.guid, re.I):
            #kick the bugger
            self.debug('Kicking %s for invalid guid (%s)' % (client.name, client.guid))
            client.kick(reason=self._kickmessage, keyword='guidcheck', data=client.guid)
        else:
            self.debug('%s appears to have a valid Guid (%s)' % (client.name, client.guid))

    def defineRegexp(self):
        if self.console.PunkBuster:
            if self._strictlength:
                _g = '^[a-z0-9]{32}$'
            else:
                _g = '^[a-z0-9]{30,32}$'
            self.verbose('Using PunkBuster ID limitations')
        #CoD4 GUID
        elif self.console.gameName == 'cod4':
            if self._strictlength:
                _g = '^[a-z0-9]{32}$'
            else:
                _g = '^[a-z0-9]{30,32}$'
            self.verbose('Using Guid limitations for %s' % self.console.gameName)
        else:
            #allow everything else
            _g = '^.*$'
            self.verbose('No compatible Guid limitations found for %s.' % self.console.gameName )
        return _g
