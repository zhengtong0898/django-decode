from django.db import models


# Create your models here.
class Topping(models.Model):
    """ Topping: 配料 """
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    """ Pizza: 披萨 """
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        topping_ids = [topping.name for topping in self.toppings.all()]
        topping_ids = ", ".join(topping_ids)
        return "%s (%s)" % (self.name, topping_ids)


class Restaurant(models.Model):
    """ Restaurant: 餐馆 """
    pizzas = models.ManyToManyField(Pizza, related_name='restaurants')
    best_pizza = models.ForeignKey(Pizza, related_name='championed_by', on_delete=models.CASCADE)
