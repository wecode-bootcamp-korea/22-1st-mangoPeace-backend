from django.urls import path

from restaurants.views import RestaurantListView

urlpatterns = [
    path("/sub_categories/<int:sub_category_id>/list", RestaurantListView.as_view()),
]