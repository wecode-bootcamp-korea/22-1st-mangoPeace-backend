from django.urls import path

from restaurants.views import RestaurantView, ReviewView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantView.as_view()),
    path("/<int:restaurant_id>/review", ReviewView.as_view()),
]