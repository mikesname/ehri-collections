"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

from portal import models

class PortalTest(TestCase):
    fixtures = ["resource.json", "repository.json", "collection.json"]
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_collection_list(self):
        """Test list of collections."""
        response = self.client.get(reverse("collection_list"))
        self.assertEqual(response.status_code, 200)

    def test_collection_detail(self):
        """Test collection detail view."""
        response = self.client.get(reverse("repo_collections", kwargs={
            "slug": "wiener-library",
        }))
        self.assertEqual(response.status_code, 200)
