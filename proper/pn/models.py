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


class Foods_in_stock(models.Model):
    Date = models.DateField()
    Document = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    Food = models.ForeignKey(Food, on_delete=models.CASCADE)
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default=1)
    Quantity = models.DecimalField(max_digits=10, decimal_places=2)
    Sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.Food} - {self.Quantity} ({self.Date})"

