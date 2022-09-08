from turtle import color
from unicodedata import name
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
User = get_user_model()

GEEKS_CHOICES =(
    ("breakfast", "Завтрак"),
    ("lunch", "Обед"),
    ("dinner", "Ужин"),
)


class Tag(models.Model):
    name = models.CharField('Имя',max_length=48, unique=True)
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
        upload_to='recipe/images/',
        null=True,
        default=None
        )
    cooking_time = models.IntegerField()
    tags = models.ManyToManyField( 
        Tag, 
        verbose_name='Тэги', 
        related_name='recipes') 



    def __str__(self):
        return f'{self.author.email}, {self.name}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='ingredient', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='recipe', on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount}'    
  

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


class FavoriteRecipe(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorite_recipe',
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в избранные.'


    @receiver(post_save, sender=User)
    def create_favorite_recipe(
            sender, instance, created, **kwargs):
        if created:
            return FavoriteRecipe.objects.create(user=instance)


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в покупки.'

    @receiver(post_save, sender=User)
    def create_shopping_cart(
            sender, instance, created, **kwargs):
        if created:
            return ShoppingCart.objects.create(user=instance)