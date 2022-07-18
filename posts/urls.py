from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.ListCreatePostView.as_view()),
    path("posts/<str:pk>/", views.PostRetrieveUpdateDestroyView.as_view()),
    path("posts/<str:pk>/answers/", views.CreateAnswerView.as_view()),
    path("posts/<str:pk>/usefull/", views.UpdateUsefullPostView.as_view()),
]
