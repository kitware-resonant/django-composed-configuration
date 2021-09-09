from typing import Type

from allauth.account import app_settings as allauth_settings
from django.contrib.auth.management.commands import createsuperuser as django_createsuperuser
from django.core.management import BaseCommand

from composed_configuration._allauth_support import (
    createsuperuser as allauth_support_createsuperuser,
)

"""
When Allauth is configured to use a User's `email` as the `username`, override the `createsuperuser`
management command to only prompt for an email address.
"""

# If using email as username
if not allauth_settings.USERNAME_REQUIRED:
    # Expose the modified command
    Command: Type[BaseCommand] = allauth_support_createsuperuser.Command
else:
    # Expose the pristine upstream version of the command
    Command = django_createsuperuser.Command
