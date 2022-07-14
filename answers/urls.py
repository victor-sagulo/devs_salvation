from django.urls import path
from . import views

urlpatterns = [
    path("answers/<int:pk>/like/", views.AnswersUpdateLikeView.as_view()),
    path("answers/<int:pk>/dislike/", views.AnswersUpdateDislikeView.as_view()),
    path("answers/<int:pk>", views.AnswerView.as_view()),
]
