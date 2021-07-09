from django.urls import path

from restaurants.views import RestaurantFoodView, RestaurantReviewView, RestaurantView, WishListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantView.as_view()),
    path("/<int:restaurant_id>/food", RestaurantFoodView.as_view()),
    path("/<int:restaurant_id>/review", RestaurantReviewView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
    # path("/review/<int:review_id>", ReviewDetailView.as_view()),
]