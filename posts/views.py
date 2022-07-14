from rest_framework import generics
from utils.mixins import SerilizerByMethodMixin
from posts.serializers import GetPostInfoSerializer, UsefullPostVoteSerializer, PostSerializer
from posts.models import Post
from posts.permissions import AuthenticatedUser, PostOwnerOrAdmPermission


class ListCreatePostView(generics.ListCreateAPIView):

    permission_classes = [AuthenticatedUser]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateUsefullPostView(generics.UpdateAPIView):

    permission_classes = [AuthenticatedUser]

    queryset = Post.objects.all()
    serializer_class = UsefullPostVoteSerializer

    def perform_update(self, serializer):
        serializer.save(data=self.request.user)


class PostRetrieveUpdateDestroyView(SerilizerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [PostOwnerOrAdmPermission]

    queryset = Post.objects.all()
    serializer_map = {
        "GET": GetPostInfoSerializer,
        "PATCH": PostSerializer,
        "DELETE": PostSerializer,
    }
