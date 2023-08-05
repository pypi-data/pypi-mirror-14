#-*- coding: utf-8 -*-
import cherrypy
from woost.models.extension import load_extensions
import --SETUP-PACKAGE--.models
import --SETUP-PACKAGE--.views
from --SETUP-PACKAGE--.controllers import --SETUP-WEBSITE--CMSController

load_extensions()
cms = --SETUP-WEBSITE--CMSController()
application = cms.mount()

