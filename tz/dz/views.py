from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response

from .models import LessonProgress, Product, ProductAccess
from .serializers import LessonProgressSerializer, ProductStatsSerializer


class LessonProgressList(generics.ListAPIView):
    serializer_class = LessonProgressSerializer

    def get_queryset(self):
        user = self.request.user
        return LessonProgress.objects.filter(user=user)


class LessonProgressByProductList(generics.ListAPIView):
    serializer_class = LessonProgressSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        return LessonProgress.objects.filter(user=user, lesson__product_id=product_id)


class ProductStats(generics.ListAPIView):
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(owner=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for product in queryset:
            lessons_progress = LessonProgress.objects.filter(lesson__product=product)
            total_watched_lessons = lessons_progress.filter(status="Просмотрено").count()
            total_watched_time = sum(progress.watched_time_seconds for progress in lessons_progress)
            total_users = User.objects.count()
            product_access_count = ProductAccess.objects.filter(product=product).count()
            purchase_percentage = (product_access_count / total_users) * 100 if total_users > 0 else 0

            data.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_watched_lessons': total_watched_lessons,
                'total_watched_time': total_watched_time,
                'total_users': total_users,
                'purchase_percentage': purchase_percentage
            })

        return Response(data)
