from django.urls       import path

from restaurants.views import RestaurantFoodsView, RestaurantReviewView, RestaurantDetailView, ReviewView, WishListView

urlpatterns = [
    path("/<int:restaurant_id>", RestaurantDetailView.as_view()),
    path("/<int:restaurant_id>/foods", RestaurantFoodsView.as_view()),
    path("/<int:restaurant_id>/reviews", RestaurantReviewView.as_view()),
    path("/<int:restaurant_id>/reviews/<int:review_id>", ReviewView.as_view()),
    path("/<int:restaurant_id>/wishlist", WishListView.as_view()),
]