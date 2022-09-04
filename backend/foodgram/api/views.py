from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (IngredientRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngredientRecipe.objects.all()
    serializer_class = IngredientRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer     
