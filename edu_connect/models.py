from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    min_users = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_link = models.URLField()

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User, related_name="groups")

    def __str__(self):
        return self.name
