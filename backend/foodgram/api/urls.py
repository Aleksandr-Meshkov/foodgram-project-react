from django.urls import include, path

from rest_framework import routers

from . import views

router_api_v1 = routers.DefaultRouter()
router_api_v1.register('tags', views.TagsViewSet, basename='tags')
router_api_v1.register(
    'ingredients', views.IngredientViewSet, basename='ingredients'
),
router_api_v1.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/subscriptions/',
        views.subscriptions_list,
        name='subscriptions'
    ),
    path(
        'users/<int:id>/subscribe/',
        views.subscriptions_detail,
        name='subscribe_detail'
    ),
    path(
        'recipes/<int:id>/favorite/',
        views.favorite_detail,
        name='favorite_detail'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        views.shopping_cart_detail,
        name='shopping_cart_detail'
    ),
    path(
        'recipes/download_shopping_cart/',
        views.download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('', include(router_api_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
