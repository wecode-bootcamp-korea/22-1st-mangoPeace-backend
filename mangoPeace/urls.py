from django.urls import path, include

urlpatterns = [
    path("users", include("users.urls")),
    path("hello", include("filters.urls")),
]