from django.db import models

from account.models import Account, Establishment
from menu.models import Meal

class OrderObject(models.Model):
    name = models.CharField(max_length=255)
    total_price = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    client_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='order_client', null=True)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name='order_establishment', null=True)

    def __str__(self):
        return self.name + " id: " + str(self.id)


class OrderMeal(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, related_name='order_meal', null=True)
    count = models.IntegerField(default=1, null=True)
    order_object = models.ForeignKey(OrderObject, on_delete=models.CASCADE, related_name='order_meal_order_object', null=True)

    def __str__(self):
        return self.meal.name + " id: " + str(self.id) + " count: " + str(self.count)
