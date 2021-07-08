from django.urls import path

from restaurants.views import CreateReviewView, RestaurantView, ReviewView, WishListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantView.as_view()),
    path("/<int:restaurant_id>/review", CreateReviewView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    path("/review/<int:review_id>", ReviewView.as_view()),
]