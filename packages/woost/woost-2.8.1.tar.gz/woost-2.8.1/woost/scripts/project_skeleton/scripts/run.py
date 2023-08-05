#!/usr/bin/env python
#-*- coding: utf-8 -*-
u"""
Launches the site's application server.
"""
from woost.models.extension import load_extensions
import --SETUP-PACKAGE--.models
import --SETUP-PACKAGE--.views
from --SETUP-PACKAGE--.controllers import --SETUP-WEBSITE--CMSController

def main():
    load_extensions()
    cms = --SETUP-WEBSITE--CMSController()
    cms.run()

if __name__ == "__main__":
    main()

