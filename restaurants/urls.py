from django.urls       import path

from restaurants.views import RestaurantFoodImageView, RestaurantFoodView, RestaurantReviewView, RestaurantDetailView, WishListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("/<int:restaurant_id>/food", RestaurantFoodView.as_view()),
    path("/<int:restaurant_id>/food/image", RestaurantFoodImageView.as_view()),
    path("/<int:restaurant_id>/review", RestaurantReviewView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
]