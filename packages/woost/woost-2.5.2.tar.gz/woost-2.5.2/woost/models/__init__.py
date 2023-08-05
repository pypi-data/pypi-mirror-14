#-*- coding: utf-8 -*-
u"""
Provides base and default content types for the woost CMS.

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			June 2008
"""
from cocktail import schema
from cocktail.events import when
from . import memberextensions

# Register the 'text/javascript' MIME type
import mimetypes
if not mimetypes.guess_extension("text/javascript"):
    mimetypes.add_type("text/javascript", ".js")
del mimetypes

@when(schema.RelationMember.attached_as_orphan)
def _hide_self_contained_relations(event):
    if event.anonymous:
        event.source.visible = False
        event.source.synchronizable = False

from woost.models.typegroups import (
    TypeGroup,
    type_groups,
    block_type_groups
)

# Base content types
#------------------------------------------------------------------------------
from .slot import Slot
from .localemember import LocaleMember
from .configuration import Configuration
from .website import Website
from .websitesession import (
    get_current_website,
    set_current_website
)
from .siteinstallation import SiteInstallation
from .changesets import ChangeSet, Change, changeset_context
from .item import Item
from .userview import UserView
from .style import Style
from .publishable import (
    Publishable,
    IsPublishedExpression,
    IsAccessibleExpression,
    UserHasAccessLevelExpression,
    user_has_access_level
)
from .document import Document
from .template import Template
from .controller import Controller
from .user import (
    User,
    AuthorizationError
)
from .usersession import (
    get_current_user,
    set_current_user
)
from .role import Role
from .accesslevel import AccessLevel
from .permission import (
    Permission,
    ContentPermission,
    CreatePermission,
    ReadPermission,
    ModifyPermission,
    DeletePermission,
    RenderPermission,
    MemberPermission,
    ReadMemberPermission,
    ModifyMemberPermission,
    CreateTranslationPermission,
    ReadTranslationPermission,
    ModifyTranslationPermission,
    DeleteTranslationPermission,
    ReadHistoryPermission,
    InstallationSyncPermission,
    restricted_modification_context,
    delete_validating,
    PermissionExpression,
    ChangeSetPermissionExpression
)
from .page import Page
from .standardpage import StandardPage
from .file import File
from .news import News
from .event import Event
from .uri import URI
from .file import File
from .extension import (
    Extension,
    extension_translations,
    load_extensions
)
from .trigger import (
    Trigger,
    ContentTrigger,
    CreateTrigger,
    InsertTrigger,
    ModifyTrigger,
    DeleteTrigger
)
from .triggerresponse import (
    TriggerResponse,
    CustomTriggerResponse,
    SendEmailTriggerResponse
)
from .emailtemplate import EmailTemplate
from .feed import Feed

from .userfilter import (
    IsPublishedFilter,
    TypeFilter
)

from .caching import CachingPolicy

from . import rendering
from .videoplayersettings import VideoPlayerSettings
from .synchronization import (
    Synchronization,
    get_manifest,
    rebuild_manifest
)
from . import staticpublication

# Blocks
from .elementtype import ElementType
from .slot import Slot
from .block import Block
from .containerblock import ContainerBlock
from .blockimagefactoryreference import BlockImageFactoryReference
from .customblock import CustomBlock
from .eventlisting import EventListing
from .facebooklikebox import FacebookLikeBox
from .facebooklikebutton import FacebookLikeButton
from .flashblock import FlashBlock
from .htmlblock import HTMLBlock
from .iframeblock import IFrameBlock
from .loginblock import LoginBlock
from .menublock import MenuBlock
from .newslisting import NewsListing
from .publishablelisting import PublishableListing
from .slideshowblock import SlideShowBlock
from .textblock import TextBlock
from .tweetbutton import TweetButton
from .twittertimelineblock import TwitterTimelineBlock
from .videoblock import VideoBlock

from . import migration

