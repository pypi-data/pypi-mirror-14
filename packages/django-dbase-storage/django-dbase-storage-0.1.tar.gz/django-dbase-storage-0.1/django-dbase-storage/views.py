from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist

from dbfile.models import DbFile

def download(request, filename):
    """
    Tell browser to open file or download if mimetype is not supported
    """

    try:
        file = DbFile.objects.find_by_filename(filename).get()
        return file.download()
    except ObjectDoesNotExist:
        raise Http404()