from django.db import models

class DatabaseFileField(models.FileField):
    """
    FileField with DatabaseStorage as default storage
    """

    description = "File in database"

    def __init__(self, *args, **kwargs):
        from .storage import DatabaseStorage
        kwargs['storage'] = DatabaseStorage()

        super(DatabaseFileField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DatabaseFileField, self).deconstruct()
        if kwargs.get("storage"):
            del kwargs["storage"]

        return name, path, args, kwargs


class BinaryFileContent(models.BinaryField):
    description = "File stored in database"

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == "sqlserver":
            return "image"
        elif connection.settings_dict['ENGINE'] == "django.db.backends.postgresql":
            return "bytea"
        else:
            return "BinaryField"


    def get_prep_lookup(self, lookup_type, value):
        raise TypeError('Lookup is not supported.')