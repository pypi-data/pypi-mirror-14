import six
import StringIO
import mimetypes

from django.core.files.storage import Storage
from gcloud import storage, exceptions

from .settings import gcs_settings as settings


class GoogleCloudStorage(Storage):
    def __init__(self, bucket=None, project=None, credentials=None, http=None):
        """
        :type bucket_name: string
        :param bucket_name: name of the bucket

        :type project: string
        :param project: the project which the client acts on.

        :type credentials: OAuth2 credentials
        :param credentials: (optional)
                            Client init will fail
                            if not passed and no `http` object provided

        :type http: :class:`httplib2.Http`
                    or callable that returns :class:`httplib2.Http`
        :param http: (optional)
                     Client init will fail
                     if not passed and no `credentials` provided
        """
        bucket = bucket or settings['bucket']
        project = project or settings['project']
        credentials = credentials or settings['credentials']
        http = http or settings['http']
        if callable(http):
            http = http()
        client = storage.Client(project, credentials, http)
        self.bucket = client.get_bucket(bucket)

    def _open(self, name):
        """
        Returns `StringIO` instance with blob file contents
        """
        output = StringIO.StringIO()
        self.bucket.get_blob(name).download_to_file(output)
        return output

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        if hasattr(content, 'content_type'):
            content_type = content.content_type
        else:
            content_type = mimetypes.guess_type(name)[0]
        blob.upload_from_file(content, True, content.size, content_type)

        blob.cache_control = ', '.join(settings['cache_control'])
        blob.patch()  # submit cache_control

        blob.make_public()
        return name

    def delete(self, name):
        try:
            self.bucket.blob(name).delete()
        except exceptions.NotFound:
            return False
        return True

    def exists(self, name):
        return self.bucket.blob(name).exists()

    def listdir(self, path=None):
        return self.bucket.list_blobs()

    def size(self, name):
        return self.bucket.blob(name).size

    def created_time(self, name):
        return self.bucket.get_blob(name)._properties.get('timeCreated')

    def modified_time(self, name):
        return self.bucket.blob(name).updated

    def url(self, name):
        """
        Unquote and quote to not have escaped slashes in url.
        """
        quote = six.moves.urllib.parse.quote
        unquote = six.moves.urllib.parse.unquote
        url, name = unquote(self.bucket.blob(name).public_url).rsplit('/', 1)
        return '{}/{}'.format(url, quote(name, safe=''))
