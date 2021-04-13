from rest_framework import serializers
from . import models

# --------------- Category -------------------------------------------------------------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id','name')


# --------------- Category -------------------------------------------------------------

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meal
        fields = ('id', 'name', 'price')



class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)
