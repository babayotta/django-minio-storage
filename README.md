[![Build Status](https://travis-ci.org/babayotta/django-minio-storage.svg?branch=master)](https://travis-ci.org/babayotta/django-minio-storage)

# django-minio-storage

Use [minio](https://minio.io) for django static and media file storage.

Minio is accessed through the Amazon S3 API, so existing django file storage
adapters for S3 should work, but in practice they are hard to configure. This
project uses the minio python client instead. Inspiration has been drawn from
`django-s3-storage` and `django-storages`.

# Documentation

See
[http://django-minio-storage.readthedocs.io/en/latest/](http://django-minio-storage.readthedocs.io/en/latest/) for
documentation and usage guides.
