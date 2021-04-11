from django.db import models

from account.models import (
    Establishment
)

class Category(models.Model):
    name = models.CharField(max_length=255)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='category_establishment', null=True)

    def __str__(self):
        return self.name + " id: " + str(self.id)


class Meal(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='meal', null=True)

    def __str__(self):
        return self.name + " id: " + str(self.id)
