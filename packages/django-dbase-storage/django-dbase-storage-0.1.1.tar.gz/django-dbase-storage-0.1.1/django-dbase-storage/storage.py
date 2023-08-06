from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.files.storage import Storage
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import connection

from io import BytesIO
from dbfile.models import DbFile


class DatabaseStorage(Storage):
    model = DbFile

    def _open(self, name, mode='rb'):
        """
        Open a file stored in the database.  name should be the full name of
        the file, including the upload_to path that may have been used.
        Path separator should always be '/'.  mode should always be 'rb'.

        Returns a Django File object if found, otherwise None.
        """
        assert mode == 'rb', "DatabaseStorage open mode must be 'rb'."

        file = self.model.objects.find_by_filename(name).get()
        return File(BytesIO(file.data))

    def _save(self, name, content):
        """
        Save the given content as file with the specified name.  Backslashes
        in the name will be converted to forward '/'.
        """
        name = name.replace('\\', '/')
        binary = content.read()
        size = len(binary)

        file = self.model(name=name, data=binary, size=size)
        file.save()

        return name

    def exists(self, name):
        return self.model.objects.find_by_filename(name).exists()

    def delete(self, name):
        self.model.objects.find_by_filename(name).delete()

    def path(self, name):
        raise NotImplementedError('DatabaseStorage does not support path().')

    def url(self, name):
        try:
            return reverse('dbfile:download', kwargs={'filename': name})
        except:
            raise ImproperlyConfigured(
                "Include url(r'^download/', include(\"dbfile.urls\", namespace=\"dbfile\") to urls")

    def size(self, name):
        """
        Get the size of the given filename or raise ObjectDoesNotExist.
        :param name: file name
        :return:
        """
        return self.model.objects.get_size(name)

    def created_time(self, name):
        """
        Returns the creation time (as datetime object) of the file
        specified by name.
        """
        return self.model.objects.get_created_time(name)
