#-*- coding: utf-8 -*-
"""Provides functions for dealing with user notifications.

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2010
"""
from warnings import warn
from cocktail.controllers import session
from cocktail.html import templates

def notify_user(message, category = None, transient = True):
    """Creates a new notification for the current user.

    Notifications are stored until a proper page is served to the user. It
    is up to the views to decide how these messages should be displayed.

    @param message: The message that will be shown to the user.
    @type message: unicode

    @param category: An optional free form string identifier that qualifies
        the message. Standard values include 'success' and 'error'.
    @type category: unicode

    @param transient: Indicates if the message should be hidden after a
        short lapse (True), or if it should remain visible until explicitly
        closed by the user (False).
    @type transient: bool
    """
    warn(
        "notify_user() is deprecated; use the Notification class instead",
        DeprecationWarning,
        stacklevel = 2
    )
    Notification(message, category, transient).emit()

def pop_user_notifications(filter = None):
    warn(
        "pop_user_notifications() is deprecated; "
        "use the Notification class instead",
        DeprecationWarning,
        stacklevel = 2
    )
    return Notification.pop(filter)


class Notification(object):

    def __init__(self, message = None, category = None, transient = False):
        self.message = message
        self.category = category
        self.transient = transient

    def __len__(self):
        # Required for backwards compatibility; notifications used to be tuples
        return 3

    def __iter__(self):
        # Required for backwards compatibility; notifications used to be tuples
        warn(
            "Notifications are no longer tuples; used the provided attributes "
            "instead",
            DeprecationWarning,
            stacklevel = 2
        )
        yield self.message
        yield self.category
        yield self.transient

    def __getitem__(self, index):
        # Required for backwards compatibility; notifications used to be tuples
        warn(
            "Notifications are no longer tuples; used the provided attributes "
            "instead",
            DeprecationWarning,
            stacklevel = 2
        )
        if index == 0:
            return self.message
        elif index == 1:
            return self.category
        elif index == 2:
            return self.transient

    def emit(self):
        """Stores the notification, so it can be retrieved by a call to
        L{pop}.
        """
        notifications = session.get("notifications")
        if notifications is None:
            session["notifications"] = [self]
        else:
            notifications.append(self)

    @classmethod
    def pop(cls, filter = None):
        """Retrieves pending notification messages that were stored through the
        L{notify_user} method.

        Retrieved messages are considered to be consumed, and therefore they
        are removed from the list of pending notifications.

        @param filter: If given, only those notifications matching the
            specified criteria will be retrieved. The criteria matches as
            follows:

                * If set to a string, it designates a single notification
                  category to retrieve.
                * If set to a subclass of L{Notification}, only notifications
                  that are instances of that type will be retrieved.
                * If set to a tuple of subclasses of L{Notification}, only
                  notifications that are instances of any of the indicated
                  types will be retrieved.
                * If set to a callable, it will be used as filter function,
                  taking a L{Notification} as its single parameter, and
                  returning True if the notification is to be retrieved, or
                  False if it should be ignored.
                * If set to a sequence (list, tuple, set), it designates a set
                  of categories; notifications belonging to any of the
                  specified categories will be retrieved.

        @return: The list of pending notification messages.
        @rtype: L{Notification} list
        """
        notifications = session.get("notifications")

        if notifications is None:
            return []

        remaining = []

        if filter:
            matching = []

            if isinstance(filter, basestring):
                match = lambda notification: notification.category == filter
            elif (
                isinstance(filter, type) and issubclass(filter, Notification)
                or (
                    isinstance(filter, tuple)
                    and filter
                    and isinstance(filter[0], type)
                    and issubclass(filter[0], Notification)
                )
            ):
                match = lambda notification: isinstance(notification, filter)
            elif callable(filter):
                match = filter
            elif hasattr("__contains__", filter):
                match = lambda notification: notification.category in filter
            else:
                raise TypeError(
                    "The 'filter' parameter for the pop_user_notifications() "
                    "function should be a string, a sequence or callable, got "
                    "%s instead" % type(filter)
                )

            for notification in notifications:
                (matching if match(notification) else remaining).append(notification)

            notifications = matching

        session["notifications"] = remaining
        return notifications

    view_class = "woost.views.Notification"

    def create_view(self):
        view = templates.new(self.view_class)
        view.notification = self
        return view

