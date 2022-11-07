from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          MySubscriptionSerializer, RecipeSerializer,
                          ShoppingCartSerializer, ShowRecipeSerializer,
                          SubscriptionSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscribe, User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscriptions_list(request):
    """
    Вывод списка подписок пользователя.
    """
    subscriptions = User.objects.filter(following__user=request.user)
    serializer = MySubscriptionSerializer(
        subscriptions, many=True, context={'request': request}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptions_detail(request, id):
    """
    Добавление, удаление подписки пользователя.
    """
    author = get_object_or_404(User, id=id)
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'author': author.id
        }
        serializer = SubscriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if Subscribe.objects.filter(user=request.user, author=author).exists():
        subscription = get_object_or_404(
            Subscribe, user=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def shopping_cart_detail(request, id):
    """
    Добавление, удаление рецепта в список покупок.
    """
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'recipe': id
        }
        serializer = ShoppingCartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if ShoppingCart.objects.filter(user=request.user, recipe=recipe).exists():
        ShoppingCart.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request, shopping_list='Shopping_list:\n\n'):
    ingredients = IngredientRecipe.objects.filter(
        recipe__shoppingcart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for ingredient in ingredients:
        shopping_list += (
            f"ingredient: {ingredient['ingredient__name']}\n"
            f"amount: {ingredient['amount']}\n"
            f"measurement unit: "
            f"{ingredient['ingredient__measurement_unit']}\n\n"
        )
    file = 'shopping_list'
    response = HttpResponse(shopping_list, 'Content-Type: application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
    return response


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_detail(request, id):
    """
    Добавление, удаление рецепта в избранные.
    """
    if request.method == 'POST':
        data = {
            'user': request.user.id,
            'recipe': id
        }
        serializer = FavoriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    recipe = get_object_or_404(Recipe, id=id)
    if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вывод тегов, тега для просмотра.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вывод списка ингредиентов, ингредиента.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Операции с рецептами: добавление/изменение/удаление/просмотр.
    """
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return ShowRecipeSerializer
        return RecipeSerializer
