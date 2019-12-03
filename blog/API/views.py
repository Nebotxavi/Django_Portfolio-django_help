from django.db.models import Q


from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView)

from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from blog.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer

from .permissions import IsOwnerOrReadOnly


class PostListAPIView(ListAPIView):
    #queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(id=query).distinct()
            # queryset_list.filter(Q(title__icontains=query)|
            # Q(content__icontains=query))
        return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
