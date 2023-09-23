from rest_framework import serializers
from tz.dz.models import LessonProgress, Product


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'


class ProductStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']