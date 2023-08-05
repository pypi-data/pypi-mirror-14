Django Google Cloud Storage
===========================
    Based on `Google Cloud Storage JSON API`_.

    Written using `Google Cloud Python Client`_ library.

.. _Google Cloud Python Client: https://github.com/GoogleCloudPlatform/gcloud-python
.. _Google Cloud Storage JSON API: https://cloud.google.com/storage/docs/json_api/

Quick start
-----------

::

    $ pip install django-gcs

Update ``settings.py``

.. code:: python

    DJANGO_GCS = {
        'bucket': 'bucket-name',
        'http': get_http_credentials
    }

Settings
--------

.. code:: python

    DJANGO_GCS = {
        'bucket': None,
        'project': '',
        'credentials': None,
        'http': None,
        'cache_control': ['no-cache']
    }

* ``bucket`` name of the bucket on google cloud storage.
* ``project`` google project name (not required).
* ``credentials`` oauth2 credentials
* ``http`` httplib2.Http instance or callable that returns httplib2.Http instance
* ``cache_control`` is a list of strings. By default ['no-cache']

*Note: One of* ``credentials`` *or* ``http`` *should be provided for authentication.*

Usage
_____

Set storage globally:

.. code:: python

    DEFAULT_FILE_STORAGE = 'django_gcs.GoogleCloudStorage'

Or per model:

.. code:: python

    from django_gcs import GoogleCloudStorage

    class FileModel(models.Model):
        file = models.ImageField(storage=GoogleCloudStorage(bucket='some-bucket'))

Example how to generate HTTP object to make request.

.. code:: python

    import pickle
    import httplib2

    def get_http_credentials():
        with open('google/oauth2/credentials/file', 'r') as f:
            credentials = pickle.load(f)
            http_credentials = credentials.authorize(httplib2.Http())
        return http_credentials