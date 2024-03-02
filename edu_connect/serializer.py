from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Product
        fields = ['name', 'start_date', 'cost', 'lesson_count']
