# Generated by Django 3.2.3 on 2022-09-08 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=48, unique=True, verbose_name='Имя'),
        ),
    ]
