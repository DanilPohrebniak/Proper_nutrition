from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Purchases(models.Model):
    Date = models.DateTimeField()
    Title = models.CharField(max_length=255)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.Title} ({self.Date})"

    class Meta:
        verbose_name_plural = "Documents"


class FoodsInStock(models.Model):
    Date = models.DateField()
    Document = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    Food = models.ForeignKey(Food, on_delete=models.CASCADE)
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default=1)
    Quantity = models.DecimalField(max_digits=10, decimal_places=3)
    Sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.Food} - {self.Quantity} ({self.Date})"


class Dish(models.Model):
    Title = models.CharField(max_length=255)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Caloric_value = models.DecimalField(max_digits=10, decimal_places=2)
    Proteins = models.DecimalField(max_digits=10, decimal_places=2)
    Fats = models.DecimalField(max_digits=10, decimal_places=2)
    Carbohydrates = models.DecimalField(max_digits=10, decimal_places=2)
    Cooking_instructions = models.TextField()
    Photo = models.ImageField(upload_to='dish_photos/')

    def __str__(self):
        return self.Title

class DishIngredient(models.Model):
    Food = models.ForeignKey('Food', on_delete=models.CASCADE)
    Unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    Quantity = models.DecimalField(max_digits=10, decimal_places=3)
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Food} - {self.Quantity} {self.Unit}"