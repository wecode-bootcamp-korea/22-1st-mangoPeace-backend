from django.urls import path

from users.views import SignInView, SignupView, UserView

urlpatterns = [
    path("/signup", SignupView.as_view()),
    path("/signin", SignInView.as_view()),
    path(("/user"), UserView.as_view()),
]