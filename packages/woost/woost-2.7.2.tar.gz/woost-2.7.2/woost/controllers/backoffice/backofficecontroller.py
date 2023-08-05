#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
"""
import cherrypy
from cocktail.pkgutils import resolve
from cocktail.events import event_handler
from cocktail.controllers import view_state
from cocktail.translations import set_language
from woost import app
from woost.models import Configuration
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController
from woost.controllers.backoffice.contentcontroller \
    import ContentController
from woost.controllers.backoffice.deletecontroller import DeleteController
from woost.controllers.backoffice.renderpreviewcontroller \
    import RenderPreviewController
from woost.controllers.backoffice.editblockscontroller \
    import EditBlocksController
from woost.controllers.backoffice.dropblockcontroller \
    import DropBlockController
from woost.controllers.backoffice.changelogcontroller \
    import ChangeLogController
from woost.controllers.backoffice.dragandropcontroller \
    import DragAndDropController
from woost.controllers.backoffice.sitesynccontroller \
    import SiteSyncController


class BackOfficeController(BaseBackOfficeController):

    _cp_config = BaseBackOfficeController.copy_config()
    _cp_config["rendering.engine"] = "cocktail"

    _edit_stacks_manager_class = \
        "woost.controllers.backoffice.editstack.EditStacksManager"

    default_section = "content"

    content = ContentController
    delete = DeleteController
    changelog = ChangeLogController
    render_preview = RenderPreviewController
    drop = DragAndDropController
    blocks = EditBlocksController
    drop_block = DropBlockController

    def submit(self):
        raise cherrypy.HTTPRedirect(
            self.contextual_uri(self.default_section) + "?" + view_state())

    @event_handler
    def handle_traversed(cls, event):
        controller = event.source
        controller.context["edit_stacks_manager"] = \
            resolve(controller._edit_stacks_manager_class)()

    @event_handler
    def handle_before_request(cls, event):
        user = app.user
        language = (
            user and user.prefered_language
            or Configuration.instance.get_setting("backoffice_language")
        )
        set_language(language)

    @event_handler
    def handle_after_request(cls, event):

        if event.error is None:
            controller = event.source
            edit_stacks_manager = controller.context["edit_stacks_manager"]
            edit_stack = edit_stacks_manager.current_edit_stack

            if edit_stack is not None:
                edit_stacks_manager.preserve_edit_stack(edit_stack)

    @cherrypy.expose
    def keep_alive(self, *args, **kwargs):
        pass

    synchronization = SiteSyncController

