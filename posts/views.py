from answers.serializers import AnswersSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.mixins import SerilizerByMethodMixin

from posts.models import Post
from posts.permissions import AuthenticatedUser, PostOwnerOrAdmPermission
from posts.serializers import (GetPostInfoSerializer, PostSerializer,
                               UsefullPostVoteSerializer)


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


class CreateAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        serializer = AnswersSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
