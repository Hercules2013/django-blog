from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from blogposts.models import BlogPost


class BlogPostViewSetTestCase(TestCase):
    """Test case for BlogPost ViewSet"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

    def test_get_list_no_blogposts(self):
        response = self.client.get(reverse("blogpost-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_list_with_blogpost(self):
        blogpost = BlogPost.objects.create(
            author=self.user, title="Fake Title", content="Fake contents"
        )
        response = self.client.get(reverse("blogpost-list"))
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "id": blogpost.pk,
            "title": blogpost.title,
            "content": blogpost.content,
            "author": blogpost.author.pk,
        }
        self.assertEqual(response.json()[0], expected_data)

    def test_create_blogpost(self):
        data = {"title": "Fake Title", "content": "Fake contents"}
        response = self.client.post(
            reverse("blogpost-list"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(BlogPost.objects.filter(title="Fake Title").exists())

    def test_create_blogpost_bad_data(self):
        data = {"title": "Fake Title", "contents": "Fake contents"}  # bad kwarg
        response = self.client.post(
            reverse("blogpost-list"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class BlogPostDetailViewSetTestCase(TestCase):
    """Test case for BlogPost Detail ViewSet"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}
        self.blogpost = BlogPost.objects.create(
            author=self.user, title="Fake Title", content="Fake contents"
        )

    def test_get_blogpost_not_exist(self):
        response = self.client.get(reverse("blogpost-detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_blogpost_exists(self):
        response = self.client.get(reverse("blogpost-detail", args=[self.blogpost.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.blogpost.title)

    def test_update_blogpost(self):
        data = {"title": "New Title"}
        response = self.client.put(
            reverse("blogpost-detail", args=[self.blogpost.pk]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.blogpost.refresh_from_db()
        self.assertEqual(self.blogpost.title, "New Title")

    def test_update_blogpost_not_exist(self):
        data = {"title": "New Title"}
        response = self.client.put(
            reverse("blogpost-detail", args=[999]),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_blogpost(self):
        response = self.client.delete(reverse("blogpost-detail", args=[self.blogpost.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BlogPost.objects.filter(pk=self.blogpost.pk).exists())

    def test_delete_blogpost_not_exist(self):
        response = self.client.delete(reverse("blogpost-detail", args=[999]))
        self.assertEqual(response.status_code, 404)
