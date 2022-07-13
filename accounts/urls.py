from django.urls import path
from . import views

urlpatterns = [
    path("accounts/login/", views.LoginView.as_view()),
    path("accounts/", views.ListCreateUserView.as_view()),
    path("accounts/<int:pk>/", views.RetrieveUpdateDestroyView.as_view()),
]
