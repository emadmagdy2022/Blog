from django.contrib import admin
from django.urls import path
from blogapi import views
from rest_framework import routers

urlpatterns = [
]
router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.PostViewSet)
urlpatterns += router.urls