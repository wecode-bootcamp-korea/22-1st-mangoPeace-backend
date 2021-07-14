from django.urls import path, include

urlpatterns = [
    path("restaurants", include("restaurants.urls")),
    path("users", include("users.urls")),
    path("filtering", include("filtering.urls")),
]
