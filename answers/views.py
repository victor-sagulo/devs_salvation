from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from answers.models import Answer
from answers.permissions import AnswerOwnerOrAdmPermission
from answers.serializers import AnswersSerializer, DislikeAnswerVote, LikeAnswerVote

# Create your views here.


class AnswersUpdateLikeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = LikeAnswerVote

    def perform_update(self, serializer):
        serializer.save(data=self.request.user)


class AnswersUpdateDislikeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = DislikeAnswerVote

    def perform_update(self, serializer):
        serializer.save(data=self.request.user)


class AnswerView(generics.RetrieveDestroyAPIView):
    permission_classes = [AnswerOwnerOrAdmPermission]

    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer