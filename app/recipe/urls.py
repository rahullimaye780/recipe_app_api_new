"""URLs for the recipe APIs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
APP_NAME = 'recipe'
urlpatterns = [
    path('', include(router.urls))
]

