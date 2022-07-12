from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.ListCreatePostView.as_view()),
    path("posts/<post_id>/", views.PostRetrieveUpdateDestroyView.as_view()),
    path("posts/<post_id>/usefull/", views.UpdateUsefullPostView.as_view()),
]
