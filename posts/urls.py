from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.ListCreatePostView.as_view()),
    path("posts/<int:pk>/", views.PostRetrieveUpdateDestroyView.as_view()),
    path("posts/<int:pk>/answers/", views.CreateAnswerView.as_view()),
    path("posts/<int:pk>/usefull/", views.UpdateUsefullPostView.as_view()),
]
