from django.urls import path
from . import views

urlpatterns = [
    path("answers/<str:pk>/like/", views.AnswersUpdateLikeView.as_view()),
    path("answers/<str:pk>/dislike/", views.AnswersUpdateDislikeView.as_view()),
    path("answers/<str:pk>/", views.AnswerView.as_view()),
]
