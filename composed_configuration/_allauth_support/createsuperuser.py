from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.management.commands import createsuperuser
from django.contrib.auth.models import User, UserManager

from composed_configuration._allauth_support.utils import temporarily_change_attributes


class Command(createsuperuser.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = EmailAsUsernameProxyUser
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

    def _validate_username(self, username, verbose_field_name, database):
        # Since "username" is actually unique, "email" (i.e. "self.username_field") is logically
        # unique too. Explicitly setting the "_unique" attribute ensures that app-level duplicate
        # checking is done by "_validate_username", which produces better, earlier error messages.
        # Out of an abundance of caution, set the "_unique" attribute back to its original value
        # when this is done.
        with temporarily_change_attributes(self.username_field, _unique=True):
            # Normalize (as it would be done before saving) for better duplicate detection
            username = self.UserModel.normalize_username(username)
            return super()._validate_username(username, verbose_field_name, database)


class EmailAsUsernameProxyUserManager(UserManager):
    # This version of "create_superuser" makes the "username" argument optional
    def create_superuser(
        self,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ) -> EmailAsUsernameProxyUser:
        # Practically, email will always be provided
        assert email
        user = super().create_superuser(
            username=email, email=email, password=password, **extra_fields
        )
        return user


class EmailAsUsernameProxyUser(User):
    class Meta(User.Meta):
        proxy = True

    objects = EmailAsUsernameProxyUserManager()

    # "createsuperuser.Command" automatically includes the referent of "USERNAME_FIELD", and we want
    # to apply username labeling, help text, and validation rules from the actual "email" field
    USERNAME_FIELD = "email"

    # Don't include "email" in "REQUIRED_FIELDS", to prevent adding that field twice to the
    # "createsuperuser.Command" argument parser
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    @classmethod
    def normalize_username(cls, username: str) -> str:
        # This method is called from "UserManager._create_user" with the actual "username" field.
        # To ensure that the saved value of the "username" field exactly matches the "email" field,
        # apply the same normalization process.
        return EmailAsUsernameProxyUserManager.normalize_email(username)
