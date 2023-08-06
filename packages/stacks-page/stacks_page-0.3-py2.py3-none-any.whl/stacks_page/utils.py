import os
from urlparse import urlparse

from django.conf import settings
from django.test.client import Client

url_prefix = getattr(settings, 'STACKSPAGE_URL_PREFIX', '/').rstrip('/')
build_directory = getattr(settings, 'STACKSPAGE_BUILD_DIRECTORY', '')


def get_StacksPage_static_save_location(instance):
    """
    Return a 2-tuple of the folder and filename of where a StacksPage
    should be saved to when publishing it as a static file based on the value
    of instance.live_url.

    Example if instance.live_url is:
    'http://www.pbs.org/wgbh/masterpiece/downtonabbey/downton-experience.html'

    Then `folder` would be 'wgbh/masterpiece/downtonabbey/' and
    `filename` would be 'downton-experience.html'
    """
    url_parsed = urlparse(instance.live_url)
    folder, filename = os.path.split(url_parsed.path)
    folder = folder.lstrip('/')
    if not filename:
        filename = 'index.html'
    return folder, filename


def get_StacksPage_local_save_path(instance):
    """
    Determine the path on disc to save static renditions of StacksPage
    instances.
    """
    folder, filename = get_StacksPage_static_save_location(instance)
    to_save_dir = os.path.join(build_directory, folder)
    if not os.path.exists(to_save_dir):
        os.makedirs(to_save_dir)
    return os.path.abspath(
        os.path.join(to_save_dir, filename)
    )


def publish_StacksPage_instance(instance):
    """Publish a StacksPage instance to a static file."""
    client = Client()
    url = instance.get_absolute_url().replace(url_prefix, '', 1)
    request = client.get(url)
    file_location = get_StacksPage_local_save_path(instance)
    f = open(file_location, 'w')
    f.write(request.content)
    f.close()
