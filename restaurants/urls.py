from django.urls import path

from restaurants.views import MainListView, RestaurantListView, HighListView

urlpatterns = [
    path("/sub_categories/<int:sub_category_id>/list", RestaurantListView.as_view()),
    path("/categories/<int:category_id>/mainlist", MainListView.as_view()),
    path("/<int:restaurant_id>/high_ratings", HighListView.as_view())
]