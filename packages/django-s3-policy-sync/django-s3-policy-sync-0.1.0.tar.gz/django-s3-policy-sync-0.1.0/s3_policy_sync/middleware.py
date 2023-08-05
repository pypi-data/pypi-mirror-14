from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
import boto
import os

def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


class S3PolicySyncMiddleware(object):

    def __init__(self):
        s3 = boto.connect_s3()
        policy_dir = getattr(settings, 'S3_POLICY_DIR')

        for bucket_name in getattr(settings, 'S3_BUCKETS', []):
            bucket = s3.get_bucket(bucket_name)
            policy = open(os.path.join(policy_dir, bucket_name)).read()
            bucket.set_policy(policy)

        # This middleware should only run once at the startup.
        # see http://stackoverflow.com/questions/2781383/where-to-put-django-startup-code
        raise MiddlewareNotUsed

