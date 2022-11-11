from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(filter.FilterSet):
    """
    Кастомный фильтр связанных моделяй, чтобы фильтрация не
    использовала первичный ключ.
    """
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )
    is_favorited = filter.BooleanFilter(
        field_name='is_favorited', method='filter_is_favorited'
    )
    is_in_shopping_cart = filter.BooleanFilter(
        field_name='is_in_shopping_cart', method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
