# coding: utf-8

from controlcenter import widgets
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch, reverse
from django.test.utils import override_settings
from . import TestCase


@override_settings(CONTROLCENTER_DASHBOARDS=())
class A_DashboardTest(TestCase):
    # Must be first
    # 'cause @override_settings doesn't override settings well :(

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'superuser', 'superuser@example.com', 'superpassword')
        self.user = User.objects.create_user(
            'user', 'user@example.com', 'password')

    def test_no_dashboard_found(self):
        self.client.login(username='superuser', password='superpassword')
        with self.assertRaises(ImproperlyConfigured):
            self.client.get(reverse('controlcenter:dashboard',
                                    kwargs={'pk': 0}))


class B_DashboardTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'superuser', 'superuser@example.com', 'superpassword')
        self.user = User.objects.create_user(
            'user', 'user@example.com', 'password')

    @override_settings(
        ROOT_URLCONF='urls',
        CONTROLCENTER_DASHBOARDS=('dashboards.EmptyDashboard',))
    def test_empty_dashboard(self):
        url = reverse('controlcenter:dashboard', kwargs={'pk': 0})
        self.client.login(username='superuser', password='superpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Can't test this, because @override_settings doesn't work here
        # Regex check. (?P<pk>0) for one and (?P<pk>[0-X]) for multiple
        # Checks for pk=1 with the only dashboard
        with self.assertRaises(NoReverseMatch):
            # I wish I could cache urls, but reverse_lazy fails with py34 & 1.8
            # https://code.djangoproject.com/ticket/25424
            reverse('controlcenter:dashboard', kwargs={'pk': 1})

        dashboard = response.context['dashboard']

        # It's empty, remember?
        # We don't check context, because `get_widgets` returns iterator
        # and it's empty now
        response = self.client.get(url)
        with self.assertRaises(StopIteration):
            next(dashboard.get_widgets(request=None))

        # Absolute url test
        self.assertEqual(dashboard.get_absolute_url(), url)

    @override_settings(
        ROOT_URLCONF='test_urls',
        CONTROLCENTER_DASHBOARDS=('dashboards.EmptyDashboard',
                                  'dashboards.NonEmptyDashboard'))
    def test_regular_dashboard(self):
        url = reverse('controlcenter:dashboard', kwargs={'pk': 1})
        # Non-staff fails
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertRedirects(response,
                             '{}?next={}'.format(reverse('admin:login'),
                                                 url))
        # Staff proceed
        self.client.login(username='superuser', password='superpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        dashboard = response.context['dashboard']
        self.assertEqual(dashboard.get_absolute_url(), url)

        # It's not empty
        self.assertIsInstance(next(dashboard.get_widgets(request=None)),
                              widgets.Group)
