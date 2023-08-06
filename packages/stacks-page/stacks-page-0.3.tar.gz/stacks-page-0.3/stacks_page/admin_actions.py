import os
from collections import Callable

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from fabric.api import env, run
from fabric.operations import put

from .utils import get_StacksPage_local_save_path, \
    get_StacksPage_static_save_location

STACKSPAGE_STATIC_PUBLISH_SERVERS = getattr(
    settings,
    'STACKSPAGE_STATIC_PUBLISH_SERVERS',
    {}
)


def spoof_run(cmd):
    """Spoff a fabric.api.run call."""
    pass


def spoof_put(local_path, remote_target_path):
    """
    Spoof fabric's put command. Copies the the file on disc at `local_path`
    into settings.STACKSPAGE_BUILD_DIRECTORY/__TEST__/`remote_target_path`
    This function is used to test StacksPagePublishServer.
    """
    remote_target = os.path.abspath(
        os.path.join(
            settings.STACKSPAGE_BUILD_DIRECTORY,
            '__TEST__',
            remote_target_path
        )
    )
    folder, filename = os.path.split(remote_target)
    os.system('mkdir -p {}'.format(folder))
    os.system('cp {} {}'.format(local_path, remote_target))


class StacksPagePublishServer(Callable):
    """
    Dynamically creates an admin action for publishing
    files to a remote server
    """

    def __init__(self, host_verbose, host_dict):
        self._use_spoof = False
        if all(
            key in host_dict for key in (
                "server", "webroot_folder", "base_url"
            )
        ):
            if host_dict.get('server') == '__testserver__':
                self._use_spoof = True

            self.host_dict = host_dict
        else:
            raise ImproperlyConfigured(
                "STACKSPAGE_STATIC_PUBLISH_SERVERS['{}'] is not set properly. "
                "Each server listed in the STACKSPAGE_STATIC_PUBLISH_SERVERS "
                "setting must provide values for 'server', 'webroot_folder' "
                "and 'base_url'".format(
                    host_verbose
                )
            )
        self.host_verbose = host_verbose
        self.short_description = (
            "Publish static files to {0}. WARNING! Cannot be undone!".format(
                host_verbose
            )
        )

    @property
    def __name__(self):
        host_verbose = slugify(self.host_verbose)
        return "publish_files_to_{}".format(
            host_verbose.replace('-', '_')
        )

    def __call__(self, modeladmin, request, queryset):
        """
        Publish a static page for each StacksPage instance in queryset and
        copies it to the server specified by host_dict
        """
        env.host_string = self.host_dict.get('server')
        queryset = queryset.filter(publish=True)
        for instance in queryset:
            instance.save()
            local_path = get_StacksPage_local_save_path(instance)
            folder, filename = get_StacksPage_static_save_location(
                instance
            )
            remote_target_dir = os.path.join(
                self.host_dict.get('webroot_folder'),
                folder
            )
            put_target = os.path.join(remote_target_dir, filename)
            if self.host_dict.get('path_processor', None) is not None:
                remote_target_dir, put_target = self.host_dict.get(
                    'path_processor'
                )(
                    remote_target_dir,
                    put_target
                )
            mkdir_cmd = 'mkdir -p {}'.format(remote_target_dir)

            if not self._use_spoof:
                run(mkdir_cmd)
                put(local_path, put_target)
            else:
                spoof_run(mkdir_cmd)
                spoof_put(local_path, put_target)
            messages.success(
                request,
                mark_safe(
                    '{0} published to <a href="{1}" target="_blank">'
                    '{1}</a>!'.format(
                        instance.title,
                        '/'.join([
                            self.host_dict.get('base_url').rstrip('/'),
                            folder,
                            filename
                        ])
                    )
                )
            )


stackspage_admin_actions = [
    StacksPagePublishServer(host_verbose, host_dict)
    for (
        host_verbose, host_dict
    ) in STACKSPAGE_STATIC_PUBLISH_SERVERS.iteritems()
]
