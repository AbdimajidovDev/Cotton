from django.urls import path

from app.users.views import LoginAPIView, LogOutAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogOutAPIView.as_view()),
]
