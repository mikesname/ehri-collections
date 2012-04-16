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

    def test_repo_list(self):
        """Test list of repositories."""
        response = self.client.get(reverse("repo_list"))
        self.assertEqual(response.status_code, 200)

    def test_collection_list(self):
        """Test list of collections."""
        response = self.client.get(reverse("collection_list"))
        self.assertEqual(response.status_code, 200)

    def test_repo_collections(self):
        """Test repository's list of collections."""
        response = self.client.get(reverse("repo_collections", kwargs={
            "slug": "wiener-library",
        }))
        self.assertEqual(response.status_code, 200)

    def test_repo_detail(self):
        """Test repo detail view."""
        response = self.client.get(reverse("repo_detail", kwargs={
            "slug": "wiener-library",
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_repo_edit(self):
        """Test repo edit view."""
        response = self.client.get(reverse("repo_edit", kwargs={
            "slug": "wiener-library",
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_collection_detail(self):
        """Test collection detail view."""
        response = self.client.get(reverse("collection_detail", kwargs={
            "slug": "caro-jella-letter-from-theresienstadt",
        }))
        self.assertEqual(response.status_code, 200)

    def test_collection_edit_get(self):
        """Test collection edit view."""
        response = self.client.get(reverse("collection_edit", kwargs={
            "slug": "caro-jella-letter-from-theresienstadt",
        }))
        self.assertEqual(response.status_code, 200)

    def test_collection_edit_post(self):
        """Test updating a collection."""
        slug = "caro-jella-letter-from-theresienstadt"
        c = models.Collection.objects.get(slug=slug)
        params = {
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk
        }
        params.update(self._get_collection_formset_metadata())
        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": slug,
        }), params)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=slug)
        self.assertEqual(c.name, "Test")
        
    def test_collection_edit_add_langprop(self):
        """Test updating a collection."""
        slug = "caro-jella-letter-from-theresienstadt"
        c = models.Collection.objects.get(slug=slug)
        self.assertNotIn("de", c.languages)
        params = {
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk
        }
        params.update(self._get_collection_formset_metadata())
        params.update({
            "language-0-value": "de",
        })

        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": slug,
        }), params)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=slug)
        self.assertIn("de", c.languages)
        
    def test_collection_edit_add_alt_name(self):
        """Test updating a collection."""
        slug = "caro-jella-letter-from-theresienstadt"
        c = models.Collection.objects.get(slug=slug)
        self.assertNotIn("Alt Test", c.other_names)
        params = {
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk
        }
        params.update(self._get_collection_formset_metadata())
        params.update({
            "othername_set-0-name": "Alt Test",
        })

        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": slug,
        }), params)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=slug)
        self.assertIn("Alt Test", c.other_names)
        
    def _get_collection_formset_metadata(self):
        meta = {}
        for field in ["date_set", "othername_set",
                "script", "script_of_description",
                "language", "language_of_description"]:
            meta["%s-INITIAL_FORMS" % field] = 0 
            meta["%s-MAX_NUM_FORMS" % field] = 1
            meta["%s-TOTAL_FORMS" % field] = 1
        return meta

