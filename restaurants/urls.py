from django.urls import path

from restaurants.views import MainListView

urlpatterns = [
    path("/categories/<int:category_id>/mainlist", MainListView.as_view()),
]