from turtle import color
from unicodedata import name

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

GEEKS_CHOICES =(
    ("breakfast", "Завтрак"),
    ("lunch", "Обед"),
    ("dinner", "Ужин"),
)


class Tag(models.Model):
    name = models.TextField(choices = GEEKS_CHOICES)
    color = models.CharField(max_length=48, unique = True)
    slug = models.SlugField(max_length = 100, unique = True)
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=225)
    measurement_unit = models.CharField(max_length=225)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe', verbose_name='Автор')
    name = models.CharField('Название рецепта', max_length=255)
    text = models.CharField('Описание рецепта', max_length=255)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredientsrecipes', through='IngredientRecipe')
    image = models.ImageField(
        'Фото рецепта',
        upload_to='static/recipe/',
        null=True,
        default=None
        )
    cooking_time = models.IntegerField()
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    
    def __str__(self):
        return f'{self.author.email}, {self.name}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='ingredients', on_delete=models.CASCADE) #  related_name='ingredients',
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE) # , related_name='recipe'
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount}'    
  

class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, related_name='tags', on_delete=models.CASCADE) #  related_name='ingredients',
    recipe = models.ForeignKey(Recipe, related_name='recipestags', on_delete=models.CASCADE) # , related_name='recipe'


class Subscribe(models.Model):	        
        
    user = models.ForeignKey(	                
        User,	               
        on_delete=models.CASCADE,	              
        related_name='follower',	                
        verbose_name='Подписчик')	                
    author = models.ForeignKey(	               
        User,	               
        on_delete=models.CASCADE,	               
        related_name='following',	               
        verbose_name='Автор')	        
        
    created = models.DateTimeField(	               
        'Дата подписки',	               
        auto_now_add=True)	        
               
        
    class Meta:	                
        verbose_name = 'Подписка'	               
        verbose_name_plural = 'Подписки'	               
        ordering = ['-id']	               
        constraints = [	               
            models.UniqueConstraint(	              
                fields=['user', 'author'],	               
                name='unique_subscription')]	               
       
    def __str__(self):
	    return f'Пользователь {self.user} -> автор {self.author}'
