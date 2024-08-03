"""
Application configuration for talentpool
"""
from django.apps import AppConfig
from django.db import models
import uuid


class UUIDAutoField(models.Field):
    """
    Custom Field for UUID
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = uuid.uuid4
        kwargs['editable'] = False
        kwargs['unique'] = True
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        """
        Return the database column data type for this field, for the provided
        connection.
        """
        return 'uuid'


def set_uuid_primary_key(model_class) -> None:
    """
    Attempt to change the default field_name to uuid from id
    :param model_class:
    :return None:
    """
    if not hasattr(model_class, 'uuid'):
        for field in model_class._meta.local_fields:
            if field.name == 'id':
                model_class._meta.local_fields.remove(field)
                break
        field = UUIDAutoField()
        field.contribute_to_class(model_class, 'uuid')
        if hasattr(model_class, '_meta'):
            model_class._meta.pk = field


class TalentpoolConfig(AppConfig):
    """
    Talentpool app configuration
    """
    name = 'talentpool'

    def ready(self) -> None:
        """
        Ready
        :return None:
        """
        from django.apps import apps
        for model in apps.get_app_config(self.name).get_models():
            set_uuid_primary_key(model)
