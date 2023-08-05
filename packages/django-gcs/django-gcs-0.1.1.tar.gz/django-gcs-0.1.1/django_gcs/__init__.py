from pkg_resources import get_distribution
from .storage import GoogleCloudStorage

__version__ = get_distribution('django-gcs').version
