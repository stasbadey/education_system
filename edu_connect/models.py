from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    min_users = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def add_student_to_group(self, student):
        if datetime.strptime(str(self.start_date), "%Y-%m-%d %H:%M") <= datetime.now():
            raise Exception("Impossible to add new student because product starts")
        groups = self.group_set.annotate(num_users=Count('users')).order_by('-num_users')

        for group in groups:
            if group.num_users < self.max_users:
                group.users.add(student)
                return

        group = Group.objects.create(product=self)  # При нехватке мест в группе создается новая группа
        group.users.add(student)

    def balance_group_try(self):
        if datetime.strptime(str(self.start_date), "%Y-%m-%d %H:%M") > datetime.now():
            self.balance_groups()
        else:
            print('Product starts')

    def balance_groups(self):
        groups = self.group_set.annotate(num_users=Count('users')).order_by('-num_users')

        while groups:
            largest_group = groups.first()
            smallest_group = groups.last()

            if largest_group.num_users - smallest_group.num_users <= 1:
                break

            # Несколько пользователей сразу перемещаются в другую группу
            users_to_move = largest_group.users.all()[:largest_group.num_users - smallest_group.num_users - 1]
            largest_group.users.remove(*users_to_move)
            smallest_group.users.add(*users_to_move)

            groups = groups.exclude(pk=largest_group.pk).exclude(pk=smallest_group.pk)
            groups = groups.annotate(num_users=Count('users')).order_by('-num_users')

    def has_user_access(self, user):
        return self.group_set.filter(users=user).exists()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=255, unique=True)
    video_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

