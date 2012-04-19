"""
Portal model unit tests.
"""

# TODO: Factor out duplication here.

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from portal import models


class EntityCrudTestCase(object):
    """Mixin class which defines a lot of boilerplate
    CRUD-deleted tests."""
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
        repo = models.Repository.objects.all()[0]
        testname = "Test Create"
        self.assertEqual(self.model.objects.filter(
                name=testname).count(), 0)
        self.testdata.update(self.updatedata)
        response = self.client.post(reverse(self.urlprefix + "_create"), self.testdata)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.model.objects.filter(
                name=testname).count(), 1)
        c = self.model.objects.filter(name=testname)[0]
        self.assertIn("en", c.languages)
        self.assertEqual(testname, c.name)
        
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
        self.assertEqual(c.name, "Test")
        
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
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update(self.updatedata)
        response = self.client.post(reverse(self.urlprefix + "_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = self.model.objects.get(slug=self.slug)
        self.assertIn("Alt Test", c.other_names)
        
    def test_edit_with_error(self):
        """Test updating a object."""
        c = self.model.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update(self.updatedata)
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
        


class PortalRepositoryTest(TestCase):
    fixtures = ["resource.json", "repository.json", "collection.json"]
    def setUp(self):
        user = User.objects.create_user("test", password="testpass")
        user.is_staff = True
        user.save()
        self.client.login(username="test", password="testpass")
        self.slug = "wiener-library"
        self.testdata = {

        }
        for field in ["contact_set", "othername_set", "script", "language"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

    def tearDown(self):
        pass

    def test_repo_list(self):
        """Test list of repositories."""
        response = self.client.get(reverse("repo_list"))
        self.assertEqual(response.status_code, 200)

    def test_repo_collections(self):
        """Test repository's list of collections."""
        response = self.client.get(reverse("repo_collections", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_repo_detail(self):
        """Test repo detail view."""
        response = self.client.get(reverse("repo_detail", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_repo_create_get(self):
        """Test repository create view."""
        response = self.client.get(reverse("repo_create"))
        self.assertEqual(response.status_code, 200)

    def test_repo_create_post(self):
        """Test creating a repository."""
        testname = "Test Create"
        self.assertEqual(models.Repository.objects.filter(
                name=testname).count(), 0)
        self.testdata.update({
            "identifier": "GB Test 0001",
            "name": testname,
            "language-0-value": "en",
        })
        response = self.client.post(reverse("repo_create"), self.testdata)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Repository.objects.filter(
                name=testname).count(), 1)
        r = models.Repository.objects.filter(name=testname)[0]
        self.assertIn("en", r.languages)
        self.assertEqual(testname, r.name)
        
    def test_repo_edit(self):
        """Test repo edit view."""
        response = self.client.get(reverse("repo_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_repository_edit_post(self):
        """Test updating a repository."""
        c = models.Repository.objects.get(slug=self.slug)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "language-0-value": "de",
        })
        response = self.client.post(reverse("repo_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Repository.objects.get(slug=self.slug)
        self.assertEqual(c.name, "Test")
        
    def test_repository_edit_add_langprop(self):
        """Test updating a repository."""
        c = models.Repository.objects.get(slug=self.slug)
        self.assertNotIn("de", c.languages)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "language-0-value": "de",
        })
        response = self.client.post(reverse("repo_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Repository.objects.get(slug=self.slug)
        self.assertIn("de", c.languages)
        
    def test_repository_edit_add_alt_name(self):
        """Test updating a repository."""
        c = models.Repository.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("repo_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Repository.objects.get(slug=self.slug)
        self.assertIn("Alt Test", c.other_names)
        
    def test_repository_edit_with_error(self):
        """Test updating a repository."""
        c = models.Repository.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "",
            "name": "Test",
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("repo_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 200)
        c = models.Repository.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)

    def test_repository_delete_confirm(self):
        """Test deleting a repository - first step."""
        response = self.client.get(reverse("repo_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_repository_delete(self):
        """Test deleting a repository - second step."""
        ccount = models.Repository.objects.count()
        response = self.client.post(reverse("repo_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)
        ccount2 = models.Repository.objects.count()
        self.assertEqual(ccount, ccount2 + 1)
        

class PortalCollectionTest(TestCase):
    fixtures = ["resource.json", "repository.json", "collection.json"]
    def setUp(self):
        user = User.objects.create_user("test", password="testpass")
        user.is_staff = True
        user.save()
        self.client.login(username="test", password="testpass")
        self.slug = "caro-jella-letter-from-theresienstadt"
        self.testdata = {

        }
        for field in ["date_set", "othername_set",
                "script", "script_of_description",
                "language", "language_of_description"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

    def tearDown(self):
        pass

    def test_collection_list(self):
        """Test list of collections."""
        response = self.client.get(reverse("collection_list"))
        self.assertEqual(response.status_code, 200)

    def test_collection_detail(self):
        """Test collection detail view."""
        response = self.client.get(reverse("collection_detail", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_collection_edit_without_credentials(self):
        """Try accessing the edit page without being a member of staff."""
        self.client.logout()
        user = User.objects.create_user("random", password="password")
        user.is_staff = False
        user.save()
        self.client.login(username=user.username, password="password")
        response = self.client.get(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)

    def test_collection_create_get(self):
        """Test collection create view."""
        response = self.client.get(reverse("collection_create"))
        self.assertEqual(response.status_code, 200)

    def test_collection_create_post(self):
        """Test creating a collection."""
        repo = models.Repository.objects.all()[0]
        testname = "Test Create"
        self.assertEqual(models.Collection.objects.filter(
                name=testname).count(), 0)
        self.testdata.update({
            "identifier": "GB Test 0001",
            "name": testname,
            "repository": repo.pk,
            "language-0-value": "en",
        })
        response = self.client.post(reverse("collection_create"), self.testdata)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Collection.objects.filter(
                name=testname).count(), 1)
        c = models.Collection.objects.filter(name=testname)[0]
        self.assertIn("en", c.languages)
        self.assertEqual(testname, c.name)
        
    def test_collection_edit_get(self):
        """Test collection edit view."""
        response = self.client.get(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_collection_edit_post(self):
        """Test updating a collection."""
        c = models.Collection.objects.get(slug=self.slug)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk
        })
        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=self.slug)
        self.assertEqual(c.name, "Test")
        
    def test_collection_edit_add_langprop(self):
        """Test updating a collection."""
        c = models.Collection.objects.get(slug=self.slug)
        self.assertNotIn("de", c.languages)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk,
            "language-0-value": "de",
        })
        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=self.slug)
        self.assertIn("de", c.languages)
        
    def test_collection_edit_add_alt_name(self):
        """Test updating a collection."""
        c = models.Collection.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "repository": c.repository.pk,
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Collection.objects.get(slug=self.slug)
        self.assertIn("Alt Test", c.other_names)
        
    def test_collection_edit_with_error(self):
        """Test updating a collection."""
        c = models.Collection.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "",
            "name": "Test",
            "repository": c.repository.pk,
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("collection_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 200)
        c = models.Collection.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)

    def test_collection_delete_confirm(self):
        """Test deleting a collection - first step."""
        response = self.client.get(reverse("collection_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_collection_delete(self):
        """Test deleting a collection - second step."""
        ccount = models.Collection.objects.count()
        response = self.client.post(reverse("collection_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)
        ccount2 = models.Collection.objects.count()
        self.assertEqual(ccount, ccount2 + 1)
        
       
class PortalAuthorityTest(TestCase):
    fixtures = ["resource.json", "authority.json"]
    def setUp(self):
        user = User.objects.create_user("test", password="testpass")
        user.is_staff = True
        user.save()
        self.client.login(username="test", password="testpass")
        self.slug = "smith-john"
        self.testdata = {

        }
        for field in ["othername_set", "script", "language"]:
            self.testdata["%s-INITIAL_FORMS" % field] = 0 
            self.testdata["%s-MAX_NUM_FORMS" % field] = 1
            self.testdata["%s-TOTAL_FORMS" % field] = 1

    def tearDown(self):
        pass

    def test_authority_list(self):
        """Test list of authorities."""
        response = self.client.get(reverse("authority_list"))
        self.assertEqual(response.status_code, 200)

    def test_authority_collections(self):
        """Test authority's list of collections."""
        response = self.client.get(reverse("authority_collections", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_authority_detail(self):
        """Test repo detail view."""
        response = self.client.get(reverse("authority_detail", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_authority_create_get(self):
        """Test authority create view."""
        response = self.client.get(reverse("authority_create"))
        self.assertEqual(response.status_code, 200)

    def test_authority_create_post(self):
        """Test creating a authority."""
        testname = "Test Create"
        self.assertEqual(models.Authority.objects.filter(
                name=testname).count(), 0)
        self.testdata.update({
            "identifier": "GB Test 0001",
            "name": testname,
            "language-0-value": "en",
        })
        response = self.client.post(reverse("authority_create"), self.testdata)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.Authority.objects.filter(
                name=testname).count(), 1)
        r = models.Authority.objects.filter(name=testname)[0]
        self.assertIn("en", r.languages)
        self.assertEqual(testname, r.name)
        
    def test_authority_edit(self):
        """Test repo edit view."""
        response = self.client.get(reverse("authority_edit", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)

    def test_authority_edit_post(self):
        """Test updating a authority."""
        c = models.Authority.objects.get(slug=self.slug)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "language-0-value": "de",
        })
        response = self.client.post(reverse("authority_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Authority.objects.get(slug=self.slug)
        self.assertEqual(c.name, "Test")
        
    def test_authority_edit_add_langprop(self):
        """Test updating a authority."""
        c = models.Authority.objects.get(slug=self.slug)
        self.assertNotIn("de", c.languages)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "language-0-value": "de",
        })
        response = self.client.post(reverse("authority_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Authority.objects.get(slug=self.slug)
        self.assertIn("de", c.languages)
        
    def test_authority_edit_add_alt_name(self):
        """Test updating a authority."""
        c = models.Authority.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "Test",
            "name": "Test",
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("authority_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 302)
        c = models.Authority.objects.get(slug=self.slug)
        self.assertIn("Alt Test", c.other_names)
        
    def test_authority_edit_with_error(self):
        """Test updating a authority."""
        c = models.Authority.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)
        self.testdata.update({
            "identifier": "",
            "name": "Test",
            "othername_set-0-name": "Alt Test",
        })
        response = self.client.post(reverse("authority_edit", kwargs={
            "slug": self.slug,
        }), self.testdata)
        self.assertEqual(response.status_code, 200)
        c = models.Authority.objects.get(slug=self.slug)
        self.assertNotIn("Alt Test", c.other_names)

    def test_authority_delete_confirm(self):
        """Test deleting a authority - first step."""
        response = self.client.get(reverse("authority_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 200)
        
    def test_authority_delete(self):
        """Test deleting a authority - second step."""
        ccount = models.Authority.objects.count()
        response = self.client.post(reverse("authority_delete", kwargs={
            "slug": self.slug,
        }))
        self.assertEqual(response.status_code, 302)
        ccount2 = models.Authority.objects.count()
        self.assertEqual(ccount, ccount2 + 1)
        


