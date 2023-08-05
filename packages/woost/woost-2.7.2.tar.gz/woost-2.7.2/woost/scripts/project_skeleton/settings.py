#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""

from woost import app
app.package = "--SETUP-PACKAGE--"
app.installation_id = "--SETUP-INSTALLATION_ID--"

# Application server configuration
import cherrypy
cherrypy.config.update({
    "global": {
        "server.socket_host": "--SETUP-APP_SERVER_HOSTNAME--",
        "server.socket_port": --SETUP-PORT--,
        "tools.encode.on": True,
        "tools.encode.encoding": "utf-8",
        "tools.decode.on": True,
        "tools.decode.encoding": 'utf-8'
    }
})

# Object store provider
from cocktail.persistence import datastore
from ZEO.ClientStorage import ClientStorage
db_host = "127.0.0.1"
db_port = --SETUP-ZEO_PORT--
datastore.storage = lambda: ClientStorage((db_host, db_port))

# Use file based sessions
from cocktail.controllers import session
session.config["session.type"] = "file"

