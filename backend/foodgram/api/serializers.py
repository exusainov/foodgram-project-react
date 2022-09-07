import base64
import datetime as dt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from typing_extensions import Required
from rest_framework.serializers import SerializerMethodField
User = get_user_model()

class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(label='Email', write_only=True)
    password = serializers.CharField(label='Пароль', style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    token = serializers.CharField(label='Токен', read_only=True)







class UserListSerializer(serializers.ModelSerializer):

   is_subscribed=serializers.BooleanField(read_only=True)

   class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')
    
   def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()            


class UserCreateSerializer(serializers.ModelSerializer):

   class Meta:
        model = User
        fields = ('email', 'id',  'username', 'first_name', 'last_name')


class UserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        label='Новый пароль')
    current_password = serializers.CharField(
        label='Текущий пароль')

    def create(self, validated_data):
        user = self.context['request'].user
        password = make_password(
            validated_data.get('new_password'))
        user.password = password
        user.save()
        return validated_data


class RecipeUserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed') 

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)


    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('measurement_unit', 'name')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('measurement_unit', 'name') 
    
    
    def to_representation(self, instance):
        data = super(IngredientSerializer, self).to_representation(instance)

        return data


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeSerializer(many=True, source='recipes')
    image = Base64ImageField(required=False, allow_null=True)    
    
    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'name', 'text', 'cooking_time', 'image', 'tags')
        read_only_fields = ('ingredients',)

    def create(self, validated_data):
        print(validated_data, 'тут')
        ingredients = validated_data.pop('recipes')
        print(ingredients, 'ТУТ')
        print(validated_data)
        recipe = Recipe.objects.create(**validated_data)

        # # Для каждого ингредиента из списка достижений

        for ingredient in ingredients:
            ingredient_id = ingredient['ingredient']['id']
            #amount = Amount.objects.create(amount=ingredient['amount'])
            current_amount = ingredient['amount']
            print(current_amount)
        # #     Создадим новую запись или получим существующий экземпляр из БД
            current_ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientRecipe.objects.create(recipe=recipe, ingredient=current_ingredient, amount=current_amount) # 
        return recipe

    def update(self, instance, validated_data):
        print(instance, 'начало')
        print(validated_data, 'начало')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )
        instance.image = validated_data.get('image', instance.image)
        # instance.recipes = validated_data.get('recipes', instance.recipes)

        # recipes = instance.recipes
        # print(recipes, 'recipes тут')
        if 'recipes' in validated_data:

            ingredients_data = validated_data.pop('recipes')

            lst = []
           
            for ingredient in ingredients_data: 
                
                print(ingredient, type(ingredient), 'тут')
                ingredient_id = ingredient['ingredient']['id']
                current_amount = ingredient['amount']
                # current_ingredient, status = Achievement.objects.get_or_create(
                #     **achievement
                #     )

                current_ingredient = Ingredient.objects.get(pk=ingredient_id)
                #print(IngredientRecipe.objects.get(recipe=instance.id, ingredient=current_ingredient, amount=current_amount))
                recipe = Recipe.objects.get(pk=instance.id)
                print(recipe.recipes, 'recipe')
                # tutu = IngredientRecipe.objects.get(recipe=recipe, ingredient=current_ingredient, amount=current_amount)
                # print(tutu.id)
                # IngredientRecipe.objects.update(id=tutu.id, recipe=recipe, ingredient=current_ingredient, amount=current_amount)    
                
                current_ingredientrecipe, status = IngredientRecipe.objects.get_or_create(recipe=recipe,
                                                                    ingredient=current_ingredient,
                                                                    amount=current_amount)
                print(status)
                if status:   
                    pass
                ingredientrecipe_id = IngredientRecipe.objects.filter(recipe=instance.id)


                print(ingredientrecipe_id)
                lst.append(current_ingredientrecipe)
                print(ingredientrecipe_id, current_ingredientrecipe, 'тут')
                print(lst, '1')
            for x in ingredientrecipe_id:
                if x not in lst:
                    x.delete()

            instance.recipes.set(lst)
            # print(instance, 'instance')

        instance.save()
        return instance

