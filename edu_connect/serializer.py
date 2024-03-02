from rest_framework import serializers
from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Product
        fields = ['name', 'start_date', 'cost', 'lesson_count']


class LessonSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['name', 'video_link', 'product']


class StatisticSerializer(serializers.ModelSerializer):
    num_students = serializers.IntegerField(read_only=True)
    group_fill_percentage = serializers.FloatField(read_only=True)
    purchase_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'num_students', 'group_fill_percentage', 'purchase_percentage']
