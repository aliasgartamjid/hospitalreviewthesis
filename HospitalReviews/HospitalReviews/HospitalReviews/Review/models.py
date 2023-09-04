from django.db import models

# Create your models here.


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)


class Review(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=500)
    label = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)