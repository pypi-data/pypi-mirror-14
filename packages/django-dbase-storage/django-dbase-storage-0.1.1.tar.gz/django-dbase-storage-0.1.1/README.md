# Database storage for Django
This package implements the Django Storage API to store any file in any database supported by Django. In many cases it is a bad idea to store files in database because performance can degrade rapidly.

## Requirements
* Python 2.7, 3+
* Django 1.7+

## Installation 
1. Install using pip:

```bash
pip install django-dbase-storage
```

2. Add to INSTALLED_APPS:

```python
    INSTALLED_APPS = (
        ...
        'dbfile',
    )
```

3. Run migrations to create table to store files

```
python manage.py migrate dbfile
```

Now you can set default storage for the whole project in settings:

```python
DEFAULT_FILE_STORAGE = 'dbfile.storage.DatabaseStorage'
```

or specify it for certain fields of your models:

```python
class UserFiles(models.Model):
    file = FileField(storage=DatabaseStorage())
```


##Known issues
DatabaseStorage fails to store file if debug-toolbar is enabled. Debug-toolbar converts binary to UTF-8 somewhere


