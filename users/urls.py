from django.urls import path

from users.views import SignInView

urlpatterns = [
    path("/signin", SignInView.as_view()),
]