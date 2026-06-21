from django.urls import path

from .views import HomePageView, CreateImagessView # new

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("imagess/", CreateImagessView.as_view(), name="add_imagess"),  # new
]
