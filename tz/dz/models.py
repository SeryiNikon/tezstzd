from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_time_seconds = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[("Просмотрено", "Просмотрено"), ("Не просмотрено", "Не просмотрено")])

    def calculate_status(self):
        if (self.watched_time_seconds / self.lesson.duration_seconds) >= 0.8:
            self.status = "Просмотрено"
        else:
            self.status = "Не просмотрено"

    def save(self, *args, **kwargs):
        self.calculate_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name} - {self.status}"
