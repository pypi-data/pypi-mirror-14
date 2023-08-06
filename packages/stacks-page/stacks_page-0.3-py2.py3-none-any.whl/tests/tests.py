from __future__ import unicode_literals

import os
from shutil import rmtree

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.test import Client, TestCase
from django.utils import six

from stacks_page.admin_actions import StacksPagePublishServer
from stacks_page.models import (
    StacksPage,
    StacksPageSection
)
from stacks_page.utils import get_StacksPage_local_save_path

DEFAULT_TEMPLATE_EXPECTED_RESPONSE = """
<html>
    <head>
        <title>Test Page</title>
        <meta name="Description" content="Test Page description.">
        <meta name="Keywords" content="">
        <link rel="canonical" href="http://www.example.com/test/" />
        <meta property="og:type" content="website"/>
        <meta property="og:title" content="Test Page" />
        <meta property="og:description" content="Test Page description." />
        <meta property="og:image"
              content="/media/media/images/canonical/testpage.png" />
        <meta property="og:url" content="http://www.example.com/test/" />
        <meta property="og:site_name" content="" />
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:site" content="">
        <meta name="twitter:creator" content="">
        <meta name="twitter:url" content="http://www.example.com/test/" />
        <meta name="twitter:title" content="Test Page" />
        <meta name="twitter:description" content="Oh hai Twitter." />
        <meta name="twitter:image"
              content="/media/media/images/canonical/testpage.png" />
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="viewport"
              content="width=device-width, initial-scale=1, minimum-scale=1">
    </head>
    <body>
        <h1>Test Page</h1>
        <h2>Test Page Navigation</h2>
        <ul>

            <li>
                <a href="#test-page-section-1">First Section</a>
            </li>

        </ul>
        <div class="content-wrapper">

            <div id="test-page-section-1">
                <h3 class="section-title">Test Page Section 1</h3>
                <h1>First Section</h1>

<p>This is the <em>first</em> <strong>section</strong>.</p>

            </div>

        </div>

</body>
</html>"""


class StacksPageTestCase(TestCase):
    """The test suite for stacks-page"""

    fixtures = ['stackspage.json']

    def setUp(self):
        password = '12345'
        # Superuser Setup
        superuser = User.objects.create_user(
            username='test_superuser',
            email='superuser@test.com',
            password=password
        )
        superuser.is_active = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        superuser_client = Client()
        superuser_login = superuser_client.login(
            username='test_superuser',
            password=password
        )
        self.assertTrue(superuser_login)
        self.superuser = superuser
        self.superuser_client = superuser_client
        # Vanilla User Setup
        user = User.objects.create_user(
            username='test_user',
            email='user@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.save()
        # Publish User Setup
        live_url_user = User.objects.create_user(
            username='live_url_user',
            email='live_url_user@test.com',
            password=password
        )
        live_url_user.is_active = True
        live_url_user.is_staff = True
        live_url_user.is_superuser = False
        live_url_user.save()
        # Adding requisite user permission
        stackspage_ct_list = ContentType.objects.get_for_models(
            StacksPage,
            StacksPageSection
        )
        stackspage_perms = Permission.objects.filter(
            content_type__in=[
                ct
                for model, ct in six.iteritems(stackspage_ct_list)
            ]
        )
        for perm in stackspage_perms:
            if perm.codename == 'can_set_stacks_page_url':
                live_url_user.user_permissions.add(perm)
            else:
                user.user_permissions.add(perm)
                live_url_user.user_permissions.add(perm)
        user_client = Client()
        user_login = user_client.login(
            username='test_user',
            password=password
        )
        self.assertTrue(user_login)
        live_url_user_client = Client()
        live_url_user_login = live_url_user_client.login(
            username='live_url_user',
            password=password
        )
        self.assertTrue(live_url_user_login)
        self.user = user
        self.user_client = user_client
        self.live_url_user_client = live_url_user_client
        self.test_page_1 = StacksPage.objects.get(pk=1)

    @classmethod
    def tearDownClass(cls):
        """
        Remove any static files created by the test suite.
        """
        rmtree(settings.STACKSPAGE_BUILD_DIRECTORY)

    def test_live_url_user_admin(self):
        """
        Test superuser admin fields
        """
        superuser_admin_response = self.superuser_client.get(
            '/admin/stacks_page/stackspage/1/'
        )
        live_url_user_admin_response = self.live_url_user_client.get(
            '/admin/stacks_page/stackspage/1/'
        )
        if six.PY2:
            superuser_response_content = superuser_admin_response.content
            live_url_user_admin_response_content = \
                live_url_user_admin_response.content
        else:
            superuser_response_content = str(superuser_admin_response.content)
            live_url_user_admin_response_content = str(
                live_url_user_admin_response.content
            )
        self.assertInHTML(
            '<label for="id_live_url">Live URL:</label>',
            superuser_response_content
        )
        self.assertInHTML(
            '<label for="id_live_url">Live URL:</label>',
            live_url_user_admin_response_content
        )

    def test_non_live_url_user_admin(self):
        """
        Test non-superuser admin fields.
        """
        admin_response = self.user_client.get(
            '/admin/stacks_page/stackspage/1/'
        )
        if six.PY2:
            user_response_content = admin_response.content
        else:
            user_response_content = str(admin_response.content)
        with self.assertRaises(AssertionError):
            self.assertInHTML(
                '<label for="id_live_url">Live URL:</label>',
                user_response_content
            )

    def test_default_template(self):
        """Test the default template."""
        self.test_page_1.publish = True
        local_save_path = get_StacksPage_local_save_path(self.test_page_1)
        self.test_page_1.save()
        f = open(local_save_path, 'r')
        self.assertHTMLEqual(
            f.read(),
            DEFAULT_TEMPLATE_EXPECTED_RESPONSE
        )

    def test_admin_action(self):
        """Test the publish admin actions."""
        self.test_page_1.publish = True
        self.test_page_1.save()
        response = self.superuser_client.post(
            '/admin/stacks_page/stackspage/',
            {
                'action': 'publish_files_to_test',
                'select_across': 0,
                'index': 0,
                '_selected_action': ['1']
            }
        )
        del response
        path_split = get_StacksPage_local_save_path(
            self.test_page_1
        ).split('stackspage_publish/')
        path_to_published = os.path.join(
            path_split[0],
            'stackspage_publish',
            '__TEST__',
            settings.STACKSPAGE_STATIC_PUBLISH_SERVERS[
                'test'
            ]['webroot_folder'],
            path_split[1]
        )
        f = open(path_to_published, 'r')
        self.assertHTMLEqual(
            f.read(),
            DEFAULT_TEMPLATE_EXPECTED_RESPONSE
        )
        self.test_page_1.publish = False
        self.test_page_1.save()

        with self.assertRaises(ImproperlyConfigured):
            x = StacksPagePublishServer('test', {'foo': 'bar'})
            del x
