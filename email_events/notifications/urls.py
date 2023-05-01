from django.urls import path

from notifications import views


urlpatterns = [
    path("", views.index, name="index"),
]