from urllib import request
from answers.serializers import AnswersSerializer
from answers.models import Answer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.mixins import SerilizerByMethodMixin

from posts.models import Post
from posts.permissions import AuthenticatedUser, PostOwnerOrAdmPermission
from posts.serializers import (
    GetPostInfoSerializer,
    PostSerializer,
    UsefullPostVoteSerializer,
)
from rest_framework.authentication import TokenAuthentication


class ListCreatePostView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AuthenticatedUser]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateUsefullPostView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AuthenticatedUser]

    queryset = Post.objects.all()
    serializer_class = UsefullPostVoteSerializer

    def perform_update(self, serializer):

        serializer.save(data=self.request.user)


class PostRetrieveUpdateDestroyView(
    SerilizerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostOwnerOrAdmPermission]

    queryset = Post.objects.all()
    serializer_map = {
        "GET": GetPostInfoSerializer,
        "PATCH": PostSerializer,
        "DELETE": PostSerializer,
    }


class CreateAnswerView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(user=self.request.user, post=post)
