from rest_framework import serializers
from . import models

from menu.serializer import MealSerializer

# --------------- Order -------------------------------------------------------------

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderObject
        fields = "__all__"

class OrderMealSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)
    class Meta:
        model = models.OrderMeal
        fields = "__all__"

