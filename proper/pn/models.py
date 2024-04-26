from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
