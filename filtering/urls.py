from django.urls import path

from filtering.views import FilteringVeiw

urlpatterns = [
    path('', FilteringVeiw.as_view()),
]