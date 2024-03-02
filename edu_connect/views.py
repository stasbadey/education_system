from datetime import datetime
from django.db.models import Count, F
from .models import Product, Group, User, Lesson
from .serializer import ProductSerializer, LessonSerializer
from rest_framework.response import Response
from rest_framework import viewsets


def create_user(username):
    user = User.objects.create(username=username)
    return user


def get_user_id(username):
    return User.objects.get(username=username)


def get_product_id(product_name):
    return Product.objects.get(name=product_name)


def create_product(creator, name, start_date, cost, min_users, max_users):
    if Product.objects.filter(name=name).exists():
        raise ValueError("A product with the same name already exists.")
    product = Product(creator=get_user_id(creator), name=name, start_date=start_date, cost=cost,
                      min_users=min_users, max_users=max_users)
    product.save()
    return product


def create_group(product, name):
    if Group.objects.filter(name=name).exists():
        raise ValueError("A group with the same name already exists.")
    group = Group(product=get_product_id(product), name=name)
    group.save()
    return group


def create_lesson(product, name, video_link=None):
    if Lesson.objects.filter(name=name).exists():
        raise ValueError("A lesson with the same name already exists.")
    lesson = Lesson(product=get_product_id(product), name=name, video_link=video_link)
    lesson.save()
    return lesson


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        upcoming_products = self.get_queryset().filter(start_date__gt=datetime.now()).annotate(
            users_count=Count('group__users')).exclude(users_count=F('max_users')).distinct()
        ongoing_products = self.get_queryset().filter(start_date__lte=datetime.now()).annotate(
            users_count=Count('group__users')).exclude(users_count__gt=F('max_users')).distinct()

        upcoming_serializer = self.get_serializer(upcoming_products, many=True)
        ongoing_serializer = self.get_serializer(ongoing_products, many=True)

        return Response({
            'upcoming_products': upcoming_serializer.data,
            'ongoing_products': ongoing_serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        lesson_count = instance.lesson_set.count()

        data = serializer.data
        data['lesson_count'] = lesson_count

        return Response(data)



class UserLessonsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        products = Product.objects.filter(group__users__username=username)
        return Lesson.objects.filter(product__in=products)
