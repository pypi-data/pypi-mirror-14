from setuptools import setup


setup(
    name='django-gcs',
    packages=['django_gcs'],
    version='0.1.1',
    description='Django file storage backend for Google Cloud Storage',
    author='Bogdan Radko',
    author_email='bodja.rules@gmail.com',
    install_requires=[
        'django',
        'gcloud == 0.11.0'
    ],
    license='MIT',
    url='https://github.com/bodja/django-gcs',
    download_url='https://github.com/bodja/django-gcs/tarball/0.1.1',
    keywords=['django', 'storage', 'gcs', 'google cloud storage'],
    classifiers=[]
)
