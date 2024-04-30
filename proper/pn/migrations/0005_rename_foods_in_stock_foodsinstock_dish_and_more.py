# Generated by Django 5.0.4 on 2024-04-30 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pn', '0004_food_unit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foods_in_stock',
            new_name='FoodsInStock',
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=255)),
                ('Caloric_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Proteins', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Fats', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Carbohydrates', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Cooking_instructions', models.TextField()),
                ('Photo', models.ImageField(upload_to='dish_photos/')),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DishIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pn.dish')),
                ('Food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pn.food')),
                ('Unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pn.unit')),
            ],
        ),
    ]
