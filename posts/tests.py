from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PostListCreateView
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class HellowWorldTestCase(APITestCase):

    def test_hellow_world(self):
        response = self.client.get(reverse("posts_home"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Hello World")


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostListCreateView.as_view()
        self.url = reverse("list_posts")
        self.user = User.objects.create(
            username="testUser", email="test@mail.com", password="test"
        )

    def test_list_post(self):
        request = self.factory.get(
            self.url
        )  # when you use self.factory it will create a demo request and then you are manually passing that request to your mentioned view
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_post_creation(self):
        sample_post = {"title": "Test Post", "content": "Test content"}
        request = self.factory.post(self.url, sample_post)
        request.user = self.user
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PostListCreateTestClientCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_posts")

    def authenticate(self):
        self.client.post(
            reverse("signup"),
            {"email": "test@mail.com", "username": "test", "password": "test"},
        )
        resp = self.client.post(
            reverse("login"),
            {"email": "test@mail.com", "password": "test"},
        )
        token = resp.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_post(self):
        response = self.client.get(
            self.url
        )  # when you use self.client it will hit the api request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_post_creation(self):
        self.authenticate()
        sample_post = {"title": "Test Post", "content": "Test content"}
        response = self.client.post(self.url, sample_post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_post["title"])
