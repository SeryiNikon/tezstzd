from django.urls import path
from .views import LessonProgressList, LessonProgressByProductList, ProductStats

urlpatterns = [
    path('lesson-progress/', LessonProgressList.as_view(), name='lesson-progress-list'),
    path('lesson-progress/<int:product_id>/', LessonProgressByProductList.as_view(), name='lesson-progress-by-product-list'),
    path('product-stats/', ProductStats.as_view(), name='product-stats'),
]
