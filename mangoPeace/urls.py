from django.urls import path, include

urlpatterns = [
    path("restaurants", include("restaurants.urls"))
]
