from django.urls import path
from emailhooks import views

urlpatterns = [
    path('', views.index),
    path('hooks/', views.hooks, name='hooks')
]
