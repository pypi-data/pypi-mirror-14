# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import force_text

from cms import api
from cms.models import CMSPlugin
from cms.utils.i18n import force_language
from cms.test_utils.testcases import URL_CMS_PLUGIN_ADD

from ..models import Person, Group
from ..cms_plugins import PeoplePlugin

from . import DefaultApphookMixin, BasePeopleTest


class TestPersonPlugins(DefaultApphookMixin, BasePeopleTest):

    def test_add_people_list_plugin_api(self):
        """
        We add a person to the People Plugin and look her up
        """
        name = 'Donald'
        Person.objects.create(name=name)
        plugin = api.add_plugin(self.placeholder, PeoplePlugin, self.language)
        plugin.people = Person.objects.all()
        self.assertEqual(force_text(plugin), force_text(plugin.pk))
        self.page.publish(self.language)

        url = self.page.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, name)

    def test_add_people_list_plugin_client(self):
        """
        We log into the PeoplePlugin
        """
        self.client.login(username=self.su_username, password=self.su_password)

        plugin_data = {
            'plugin_type': 'PeoplePlugin',
            'plugin_language': self.language,
            'placeholder_id': self.placeholder.pk,
        }

        response = self.client.post(URL_CMS_PLUGIN_ADD, plugin_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CMSPlugin.objects.exists())

    def test_hide_ungrouped(self):
        """
        """
        the_bradys = Group.objects.create(name="The Bradys")
        alice = Person.objects.create(name="Alice")
        bobby = Person.objects.create(name="Bobby")
        cindy = Person.objects.create(name="Cindy")
        # Alice is the housekeeper, not a real Brady.
        bobby.groups.add(the_bradys)
        cindy.groups.add(the_bradys)

        # Add a plugin where ungrouped people are not shown
        plugin = api.add_plugin(self.placeholder, PeoplePlugin, self.language)
        plugin.people = Person.objects.all()
        plugin.group_by_group = True
        plugin.show_ungrouped = False
        plugin.save()

        self.page.publish(self.language)
        url = self.page.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, bobby.name)
        self.assertContains(response, cindy.name)
        self.assertNotContains(response, alice.name)

    def test_show_ungrouped(self):
        """
        """
        the_bradys = Group.objects.create(name="The Bradys")
        alice = Person.objects.create(name="Alice")
        bobby = Person.objects.create(name="Bobby")
        cindy = Person.objects.create(name="Cindy")
        # Alice is the housekeeper, not a real Brady.
        bobby.groups.add(the_bradys)
        cindy.groups.add(the_bradys)

        # Now, add a new plugin where ungrouped people are shown
        plugin = api.add_plugin(self.placeholder, PeoplePlugin, self.language)
        plugin.people = Person.objects.all()
        plugin.group_by_group = True
        plugin.show_ungrouped = True
        plugin.save()

        self.page.publish(self.language)
        url = self.page.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, bobby.name)
        self.assertContains(response, cindy.name)
        self.assertContains(response, alice.name)


class TestPeopleListPluginNoApphook(BasePeopleTest):

    def test_plugin_with_no_apphook_doesnot_breaks_page(self):
        with force_language('en'):
            name = 'Donald'
            Person.objects.create(name=name)
            api.add_plugin(
                self.placeholder, PeoplePlugin, 'en')
            self.page.publish('en')
            url = self.page.get_absolute_url()
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)
        from ..cms_plugins import NAMESPACE_ERROR
        self.assertNotContains(response, NAMESPACE_ERROR[:20])

    def test_plugin_with_no_apphook_shows_error_message(self):
        with force_language('en'):
            name = 'Donald'
            Person.objects.create(name=name)
            api.add_plugin(
                self.placeholder, PeoplePlugin, 'en')
            self.page.publish('en')
            url = self.page.get_absolute_url()
            self.client.login(username=self.su_username,
                              password=self.su_password)
            response = self.client.get(url, user=self.superuser)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)
        from ..cms_plugins import NAMESPACE_ERROR
        self.assertContains(response, NAMESPACE_ERROR[:20])
