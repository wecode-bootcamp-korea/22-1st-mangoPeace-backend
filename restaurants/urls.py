from django.urls import path

from restaurants.views import RestaurantFoodImageView

urlpatterns = [
    path("/<int:restaurant_id>/food/image", RestaurantFoodImageView.as_view()),
]