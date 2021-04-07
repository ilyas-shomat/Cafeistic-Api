from django.db import models

from account.models import (
    Establishment
)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='category_establishment', null=True)

    def __str__(self):
        return self.name
