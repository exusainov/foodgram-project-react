from turtle import color
from unicodedata import name

from django.db import models

GEEKS_CHOICES =(
    ("breakfast", "Завтрак"),
    ("lunch", "Обед"),
    ("dinner", "Ужин"),
)
# Create your models here.

# class Amount(models.Model):
#     amount = models.IntegerField()
   
#     def __str__(self):
#         return f'{self.amount}'

class Tag(models.Model):
    name = models.TextField(choices = GEEKS_CHOICES)
    color = models.CharField(max_length=48)
    slug = models.SlugField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=48)
    measurement_unit = models.CharField(max_length=48)
    
    def foo(self):
        return self.name
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=48)
    text = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredientsrecipes', through='IngredientRecipe')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,  
        default=None
        )
    cooking_time = models.IntegerField()
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='ingredients', on_delete=models.CASCADE) #  related_name='ingredients',
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE) # , related_name='recipe'
    amount = models.IntegerField()

    # def get_full_address(self):
    #     return "%s, %s" % (self.amount, self.ingredients) 
    # def get_name(self):
    #     return self.ingredient.name

    def __str__(self):
        return f'{self.amount}'    
  

class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, related_name='tags', on_delete=models.CASCADE) #  related_name='ingredients',
    recipe = models.ForeignKey(Recipe, related_name='recipestags', on_delete=models.CASCADE) # , related_name='recipe'

# class AmountIngredient(models.Model):
#     ingredient = models.ForeignKey(Ingredient, related_name='ingredients', on_delete=models.CASCADE)
#     amount = models.ForeignKey(IngredientRecipe, related_name='ingredientrecipe', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.ingredient
