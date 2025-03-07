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
from accounts.serializers import CurrentUserPostsSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

# posts = [
#     {"pk": 1, "title": "TestTitle", "content": "test", "auhtor": "test"},
#     {"pk": 2, "title": "TestTitle", "content": "test", "auhtor": "test"},
#     {"pk": 3, "title": "TestTitle", "content": "test", "auhtor": "test"},
# ]


class CustomPaginator(PageNumberPagination):
    page_size = 4
    page_query_param = "page"
    page_size_query_param = "page_size"


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
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    @swagger_auto_schema(
        operation_summary="List All Posts",
        operation_description="This will return list of all posts",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Creates Post",
        operation_description="This will create posts",
    )
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
    permission_classes = [AuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Retrive Post by ID",
        operation_description="This will Retrive Post by ID",
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Post by ID",
        operation_description="This will Update Post by ID",
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Post by ID",
        operation_description="This will Delete Post by ID",
    )
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


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostsSerializer(instance=user, context={"request": request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None
        # user = self.kwargs.get("username")
        queryset = Post.objects.all()
        if username:
            return Post.objects.filter(author__username=username)

        return queryset

    @swagger_auto_schema(
        operation_summary="List Posts of User",
        operation_description="This will list all posts of user",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
