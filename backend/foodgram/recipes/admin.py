from django.contrib import admin

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class Ingredients(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'cooking_time', 'favorites', 'amount_ingredients'
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags',)
    inlines = (Ingredients,)

    def favorites(self, obj):
        if obj.favorites.exists():
            return obj.favorites.count()
        return 0

    favorites.short_description = 'Избранное'

    def amount_ingredients(self, obj):
        if obj.ingredients.exists():
            return ', '.join(
                [str(ingredient) for ingredient in obj.ingredients.all()]
            )
        return 0

    amount_ingredients.short_description = 'Ингредиенты'


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']
    search_fields = ['name', 'slug']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
