#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Pepe Osca <pepe.osca@whads.com>
"""
from ZODB.POSException import ConflictError
from cocktail.events import Event
from cocktail import schema
from cocktail.persistence import transaction
from woost import app
from woost.models import Item, User

MAX_COMMIT_ATTEMPTS = 5


class IdentityProvider(Item):

    instantiable = False
    visible_from_root = False

    user_authenticated = Event(
        """An event triggered when the provider resolves a user.

        .. attribute:: user

            The `user <woost.models.User>` resolved by the provider.

        .. attribute:: data

            The user's profile data supplied by the provider (a dictionary with
            provider specific keys).

        .. attribute:: first_login

            Indicates if this is the first time that this user has logged in
            using this provider.
        """
    )

    members_order = [
        "title",
        "debug_mode"
    ]

    title = schema.String(
        descriptive = True
    )

    debug_mode = schema.Boolean(
        required = True,
        default = False
    )

    provider_name = None
    user_data_id_field = "id"
    user_data_email_field = "email"
    user_identifier = None

    def get_auth_url(self, target_url = None):
        raise ValueError(
            "%s doesn't implement the get_auth_url() method"
            % self
        )

    def login(self, data):
        user = transaction(self.process_user_data, (data,))
        app.authentication.set_user_session(user)
        return user

    def process_user_data(self, data):

        id = data[self.user_data_id_field]
        email = data.get(self.user_data_email_field)
        user = (
            User.get_instance(**{self.user_identifier: id})
            or (
                email
                and User.get_instance(email = email)
            )
        )

        if user is None:
            user = User()

        if not user.get(self.user_identifier):
            user.set(self.user_identifier, id)
            if not user.email:
                user.email = email
            first_login = True
        else:
            first_login = False

        self.user_authenticated(
            user = user,
            data = data,
            first_login = first_login
        )
        user.insert()
        return user

