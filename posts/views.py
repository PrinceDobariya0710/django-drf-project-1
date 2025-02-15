from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from posts.models import Post
from posts.serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permissions import ReadOnly

# Create your views here.

# posts = [
#     {"pk": 1, "title": "TestTitle", "content": "test", "auhtor": "test"},
#     {"pk": 2, "title": "TestTitle", "content": "test", "auhtor": "test"},
#     {"pk": 3, "title": "TestTitle", "content": "test", "auhtor": "test"},
# ]


# When you use Request and Response from DRF its mandatory to use DRF's views
@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def hello(request: Request):
    if request.method == "POST":
        data = request.data
        return Response(status=status.HTTP_201_CREATED, data=data)
    res = {"message": "Hello World"}
    return Response(status=status.HTTP_200_OK, data=res)


# @api_view(http_method_names=["GET", "POST"])
# def list_posts(request: Request):
#     if request.method == "POST":
#         data = request.data
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message": "Post Created", "data": serializer.data}
#             return Response(status=status.HTTP_201_CREATED, data=response)
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST, data={"message": serializer.errors}
#         )
#     posts = Post.objects.all()
#     serializer = PostSerializer(instance=posts, many=True)
#     response = {"message": "posts", "data": serializer.data}
#     return Response(status=status.HTTP_200_OK, data=response)


# @api_view(http_method_names=["GET"])
# def post_detail(request: Request, post_id: int):
#     post = get_object_or_404(Post, pk=post_id)
#     serializer = PostSerializer(instance=post)
#     response = {"message": "posts", "data": serializer.data}
#     return Response(status=status.HTTP_200_OK, data=response)


# @api_view(http_method_names=["PUT"])
# def update_post(request: Request, post_id: int):
#     post = get_object_or_404(Post, pk=post_id)
#     data = request.data
#     serializer = PostSerializer(instance=post, data=data)
#     if serializer.is_valid():
#         serializer.save()
#         response = {"message": "Post Updated", "data": serializer.data}
#         return Response(status=status.HTTP_200_OK, data=response)
#     return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


# @api_view(http_method_names=["DELETE"])
# def delete_post(request: Request, post_id: int):
#     post = get_object_or_404(Post, pk=post_id)
#     post.delete()
#     response = {"message": "Post Deleted"}
#     return Response(status=status.HTTP_204_NO_CONTENT, data=response)

# Sipmple Class Based Views
# class PostListCreateView(APIView):
#     """
#     A class based view to create and list all posts
#     """

#     serializer_class = PostSerializer

#     def get(self, request: Request, *args, **kwargs):
#         posts = Post.objects.all()
#         serializer = self.serializer_class(instance=posts, many=True)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)

#     def post(self, request: Request, *args, **kwargs):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message": "Post Created", "data": serializer.data}
#             return Response(status=status.HTTP_201_CREATED, data=response)
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST, data={"message": serializer.errors}
#         )


# class PostRetriveUpdateDeletView(APIView):
#     serializer_class = PostSerializer

#     def get(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)
#         serializer = self.serializer_class(instance=post)
#         response = {"message": "posts", "data": serializer.data}
#         return Response(status=status.HTTP_200_OK, data=response)

#     def put(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)
#         data = request.data
#         serializer = self.serializer_class(instance=post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message": "Post Updated", "data": serializer.data}
#             return Response(status=status.HTTP_200_OK, data=response)
#         return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

#     def delete(self, request: Request, post_id: int):
#         post = get_object_or_404(Post, pk=post_id)
#         post.delete()
#         response = {"message": "Post Deleted"}
#         return Response(status=status.HTTP_204_NO_CONTENT, data=response)


class PostListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """
    A class based view to create and list all posts
    """

    serializer_class = PostSerializer
    permission_classes = [ReadOnly]
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetriveUpdateDeletView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# class PostViewSet(viewsets.ViewSet):

# def list(self, request: Request):
#     queryset = Post.objects.all()
#     serializer = PostSerializer(instance=queryset, many=True)
#     return Response(status=status.HTTP_200_OK, data=serializer.data)

# def rertive(self, request: Request, pk=None):
#     post = get_object_or_404(Post, pk=pk)
#     serializer = PostSerializer(instance=post)
#     response = {"message": "posts", "data": serializer.data}
#     return Response(status=status.HTTP_200_OK, data=response)


# With ModelViewSet you can create your CRUD API in just 3 lines of code
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
