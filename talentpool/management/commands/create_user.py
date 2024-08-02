"""
Create User Management Command
"""

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from talentpool.application.services import UserService


class Command(BaseCommand):
    """
    Create User Management Command
    """
    help = 'Create a new user'

    def add_arguments(self, parser):
        """
        Add command arguments
        :param parser:
        :return:
        """
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('password', type=str, help='Password of the user')

    def handle(self, *args, **kwargs):
        """
        Handle command
        :param args:
        :param kwargs:
        :return:
        """
        username = kwargs['username']
        password = kwargs['password']

        data = {
            'username': username,
            'password': password,
        }

        try:
            user, token = UserService.create_user(data)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created user {user.username} with token {token.key}'))
        except ValidationError as e:
            self.stderr.write(self.style.ERROR(f'Error creating user: {e.messages}'))
