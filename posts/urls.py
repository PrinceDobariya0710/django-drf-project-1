from django.urls import path
from posts import views

urlpatterns = [
    path("homepage/", views.hello, name="posts_home"),
    path("", views.PostListCreateView.as_view(), name="list_posts"),
    path("<int:pk>/", views.PostRetriveUpdateDeletView.as_view(), name="post_detail"),
]
