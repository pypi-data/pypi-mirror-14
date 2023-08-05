#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import cherrypy
from simplejson import dumps
from cocktail.translations import language_context, translations
from cocktail.persistence import PersistentObject
from cocktail.controllers import Controller


class CMSMetadataController(Controller):

    def __call__(self, language, format = "json"):

        with language_context(language):

            data = {"types": {}}

            for cls in PersistentObject.schema_tree():

                if cls.translation_source is not None:
                    continue

                type_info = {
                    "name": cls.name,
                    "namespace": cls.__module__,
                    "label": translations(cls.name),
                    "plural": translations(cls.name + "-plural")
                }

                for base in cls.__bases__:
                    if issubclass(base, PersistentObject):
                        type_info["base"] = \
                            base.get_qualified_name(include_ns = True)
                        break

                full_name = cls.get_qualified_name(include_ns = True)
                data["types"][full_name] = type_info

            if format == "json":
                cherrypy.response.headers["Content-Type"] = "application/json"
                return dumps(data)
            elif format == "javascript":
                cherrypy.response.headers["Content-Type"] = "text/javascript"
                javascript = [u"cocktail.declare('woost.metadata');"]
                for key, value in data.iteritems():
                    javascript.append(
                        u"woost.metadata.%s = %s;"
                        % (key, dumps(value))
                    )
                return u"\n".join(javascript)
            else:
                raise ValueError(
                    "The 'format' parameter should be one of 'json' or "
                    "'javascript'; got %r instead" % format
                )

