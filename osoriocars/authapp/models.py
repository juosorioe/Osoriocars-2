from django.contrib.auth.models import AbstractUser
# authapp/models.py

from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=100)  # Asumiendo que estás usando nombres de archivos de imagen

    def __str__(self):
        return self.title
# Otros modelos...

class CustomUser(AbstractUser):
    is_mechanic = models.BooleanField(default=False)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, related_name='orders', through='OrderService')
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_total(self):
        self.total_price = sum(service.price for service in self.services.all())
        self.save()

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'


class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
