from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from answers.models import Answer
from answers.permissions import AnswerOwnerOrAdmPermission
from answers.serializers import AnswersSerializer, DislikeAnswerVote, LikeAnswerVote
from rest_framework.authentication import TokenAuthentication

# Create your views here.


class AnswersUpdateLikeView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = LikeAnswerVote

    def perform_update(self, serializer):
        serializer.save(data=self.request.user)


class AnswersUpdateDislikeView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = DislikeAnswerVote

    def perform_update(self, serializer):
        serializer.save(data=self.request.user)


class AnswerView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AnswerOwnerOrAdmPermission]

    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer
