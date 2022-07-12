from rest_framework import generics
from utils.mixins import SerilizerByMethodMixin
from posts.serializers import GetPostInfoSerializer, UsefullPostVoteSerializer, PostSerializer
from posts.models import Post


class ListCreatePostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateUsefullPostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UsefullPostVoteSerializer


class PostRetrieveUpdateDestroyView(SerilizerByMethodMixin, generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_map = {
        "GET": GetPostInfoSerializer,
        "PATCH": PostSerializer,
        "DELETE": PostSerializer,
    }
