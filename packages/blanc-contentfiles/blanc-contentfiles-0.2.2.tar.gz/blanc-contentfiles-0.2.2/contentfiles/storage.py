from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.six.moves import urllib
from storages.backends.s3boto import S3BotoStorage


CONTENTFILES_SSL = getattr(settings, 'CONTENTFILES_SSL', False)
CONTENTFILES_PREFIX = getattr(settings, 'CONTENTFILES_PREFIX')
CONTENTFILES_HOSTNAME = getattr(settings, 'CONTENTFILES_HOSTNAME', None)


class BaseContentFilesStorage(S3BotoStorage):
    location = '%s/' % (CONTENTFILES_PREFIX,)
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    file_overwrite = False


class MediaStorage(BaseContentFilesStorage):
    bucket_name = os.environ.get('CONTENTFILES_DEFAULT_BUCKET')

    def url(self, name):
        protocol = 'https' if CONTENTFILES_SSL else 'http'

        if CONTENTFILES_HOSTNAME is None:
            hostname = '%s.contentfiles.net' % (CONTENTFILES_PREFIX,)
        else:
            hostname = CONTENTFILES_HOSTNAME

        return '%s://%s/media/%s' % (
            protocol, hostname, urllib.parse.quote(name.encode('utf-8')))


class PrivateStorage(BaseContentFilesStorage):
    bucket_name = os.environ.get('CONTENTFILES_PRIVATE_BUCKET')
    default_acl = 'private'
    querystring_expire = 300
