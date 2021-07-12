from django.urls import path

from users.views import SignInView, SignupView

urlpatterns = [
    path("/signin", SignInView.as_view()),
    path("/signup", SignupView.as_view()),
]