"""
Portal model unit tests.
"""

# TODO: Factor out duplication here.

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from portal import models


class EntityCrudTestMixin(object):
    """Mixin class which defines a lot of boilerplate
    CRUD-deleted tests."""
    def create_user_and_login(self):
        """Create a staff user to perform admin actions."""
        user = User.objects.create_user("test", password="testpass")
        user.is_staff = True
        user.save()
        self.client.login(username="test", password="testpass")

    def test_list(self):
        """Test list of objects."""
        response = self.client.get(reverse(self.urlprefix + "_list"))
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        """Test object detail view."""
        response = self.client.get(reverse(self.urlprefix + "_detail", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_edit_without_credentials(self):
        """Try accessing the edit page without being a member of staff."""
        self.client.logout()
        user = User.objects.create_user("random", password="password")
        user.is_staff = False
        user.save()
        self.client.login(username=user.username, password="password")
        response = self.client.get(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)

    def test_create_get(self):
        """Test object create view."""
        response = self.client.get(reverse(self.urlprefix + "_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        """Test creating a object."""
        self.assertEqual(self.model.objects.filter(
                name=self.updatedata["name"]).count(), 0)
        self.testdata.update(self.updatedata)
        response = self.client.post(reverse(self.urlprefix + "_create"), self.testdata)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.model.objects.filter(
                name=self.updatedata["name"]).count(), 1)
        c = self.model.objects.filter(name=self.updatedata["name"])[0]
        self.assertIn("en", c.languages)
        self.assertEqual(self.updatedata["name"], c.name)
        
    def test_edit_get(self):
        """Test  edit view."""
        response = self.client.get(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        """Test updating a object."""
        c = self.model.objects.get(slug=self.slug)
        self.testdata.update(self.updatedata)
        response = self.client.post(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = self.model.objects.get(slug=self.slug)
        self.assertEqual(c.name, self.updatedata["name"])
        
    def test_edit_add_langprop(self):
        """Test updating a object."""
        c = self.model.objects.get(slug=self.slug)
        self.assertNotIn("de", c.languages)
        self.testdata.update(self.updatedata)
        self.testdata.update({
            "language-0-value": "de",
        })
        response = self.client.post(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = self.model.objects.get(slug=self.slug)
        self.assertIn("de", c.languages)
        
    def test_edit_add_alt_name(self):
        """Test updating a object."""
        c = self.model.objects.get(slug=self.slug)
        self.assertNotIn("Another Name", c.other_names)
        self.testdata.update(self.updatedata)
        self.testdata.update({
            "othername_set-0-name": "Another Name",
        })
        response = self.client.post(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = self.model.objects.get(slug=self.slug)
        self.assertIn("Another Name", c.other_names)
        
    def test_edit_with_error(self):
        """Test updating a object."""
        c = self.model.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update(self.updatedata)
        # send a blank identifier - this should be an error
        self.testdata["identifier"] = ""
        response = self.client.post(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 200)
        c = self.model.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)

    def test_delete_confirm(self):
        """Test deleting a object - first step."""
        response = self.client.get(reverse(self.urlprefix + "_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_delete(self):
        """Test deleting a object - second step."""
        ccount = self.model.objects.count()
        response = self.client.post(reverse(self.urlprefix + "_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)
        ccount2 = self.model.objects.count()
        self.assertEqual(ccount, ccount2 + 1)
        

class PortalRepositoryTest(TestCase, EntityCrudTestMixin):
    fixtures = ["resource.json", "repository.json", "collection.json"]
    def setUp(self):
        self.create_user_and_login()
        self.model = models.Repository
        self.slug = "wiener-library"
        self.urlprefix = "repo"
        self.testdata = {}
        self.updatedata = {
            "identifier": "Test",
            "name": "Test",
            "language-0-value": "en",
        }
        for field in ["contact_set", "othername_set", "script", "language"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

    def test_repo_collections(self):
        """Test repository's list of collections."""
        response = self.client.get(reverse("repo_collections", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        

class PortalCollectionTest(TestCase, EntityCrudTestMixin):
    fixtures = ["resource.json", "repository.json", "collection.json"]
    def setUp(self):
        self.create_user_and_login()
        self.model = models.Collection
        self.urlprefix = "collection"
        self.slug = "caro-jella-letter-from-theresienstadt"
        self.testdata = {}
        self.updatedata = {
            "identifier": "GB Test 0001",
            "name": "Test Collection",
            "repository": self.model.objects.get(slug=self.slug).repository.pk,
            "language-0-value": "en",
        }
        for field in ["date_set", "othername_set",
                "script", "script_of_description",
                "language", "language_of_description"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

       
class PortalAuthorityTest(TestCase, EntityCrudTestMixin):
    fixtures = ["resource.json", "authority.json"]
    def setUp(self):
        self.create_user_and_login()
        self.model = models.Authority
        self.urlprefix = "authority"
        self.slug = "smith-john"
        self.testdata = {}
        self.updatedata = {
            "identifier": "GB Test 0001",
            "name": "Auth Test",
            "language-0-value": "en",
        }
        for field in ["othername_set", "script", "language"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

    def tearDown(self):
        pass

    def test_authority_collections(self):
        """Test authority's list of collections."""
        response = self.client.get(reverse("authority_collections", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
