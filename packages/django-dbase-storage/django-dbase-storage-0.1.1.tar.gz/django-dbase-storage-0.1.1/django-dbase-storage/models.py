from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db.models.signals import post_delete
from django.utils.crypto import get_random_string
import os

from django.db import models, IntegrityError

from .fields import BinaryFileContent

class DbFileManager(models.Manager):
    def find_by_filename(self, name):
        # Fix paths produced on Windows
        name = name.replace('\\', '/')

        return self.get_queryset().filter(name=name)

    def _get_field_value(self, column, filename):
        """
        Get value of one field only. This is useful because we don't want to fetch blobs with file content
        :param column: string
        :param filename: string
        :return:
        """

        table_name = self.model._meta.db_table
        query = "SELECT id, %s FROM %s WHERE name = %%s" % (column, table_name)

        try:
            row = self.raw(query, [filename])[0]
        except:
            raise ObjectDoesNotExist("DatabaseStorage file not found: %s" % filename)

        return getattr(row, column)

    def get_size(self, name):
        return self._get_field_value("size", name)

    def get_created_time(self, name):
        return self._get_field_value("size", name)


class DbFile(models.Model):
    """
    Model to store files in
    """

    class Meta:
        db_table = 'dbfile'

    name = models.CharField("File name", max_length=255, unique=True)
    size = models.PositiveIntegerField("File size")
    data = BinaryFileContent("Content")
    created = models.DateTimeField("Creation date", auto_now_add=True)

    objects = DbFileManager()


    def download(self):
        """
        Output to http response
        :return:
        """
        import mimetypes
        from django.http import HttpResponse


        # Prepare response
        content_type, content_encoding = mimetypes.guess_type(self.name)
        response = HttpResponse(content=self.data, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename=%s' % self.name
        if content_encoding:
            response['Content-Encoding'] = content_encoding

        return response

