from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Recipe)

admin.site.register(IngredientRecipe)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagRecipe)
