from django_filters import rest_framework as filter

from recipes.models import Recipe, Tag
from users.models import User


class RecipeFilter(filter.FilterSet):
    """
    Кастомный фильтр связанных моделяй, чтобы фильтрация не
    использовала первичный ключ.
    """
    author = filter.ModelChoiceFilter(
        field_name='author__username',
        queryset=User.objects.all(),
        label='Author',
        to_field_name='username'
    )
    name = filter.CharFilter()
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'tags')
