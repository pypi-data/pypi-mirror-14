#-*- coding: utf-8 -*-
"""

@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			Jun 2009
"""
import os
from unittest import TestCase
from cocktail.tests.persistence.tempstoragemixin import TempStorageMixin

class BaseTestCase(TempStorageMixin, TestCase):

    def setUp(self):

        from woost import app
        from woost.models import Configuration, User, Role
        from woost.models.trigger import get_triggers_enabled, set_triggers_enabled
        from woost.controllers.installer import Installer

        self.__prev_installation_id = app.installation_id
        self.__prev_triggers_enabled = get_triggers_enabled()
        app.installation_id = "TEST"
        set_triggers_enabled(False)

        TempStorageMixin.setUp(self)

        app.root = os.path.join(self._temp_dir, "test_project")
        installer = Installer()
        installer.create_project({"project_path": app.root})

        # Configuration
        self.config = Configuration(qname = "woost.configuration")
        self.config.insert()

        # Roles and users
        self.anonymous_role = Role(qname = "woost.anonymous")
        self.anonymous_role.insert()

        self.anonymous_user = User(qname = "woost.anonymous_user")
        self.anonymous_user.roles.append(self.anonymous_role)
        self.anonymous_user.insert()

        self.everybody_role = Role(qname = "woost.everybody")
        self.everybody_role.insert()

        self.authenticated_role = Role(qname = "woost.authenticated")
        self.authenticated_role.insert()

        set_triggers_enabled(True)

    def tearDown(self):
        from woost import app
        from woost.models import staticpublication
        from woost.models.trigger import set_triggers_enabled

        app.installation_id = self.__prev_installation_id
        set_triggers_enabled(self.__prev_triggers_enabled)

        TempStorageMixin.tearDown(self)

