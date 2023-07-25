from django.db import models
from django.contrib.auth import get_user_model

from django_base64field.fields import Base64Field

User = get_user_model()
MOOD_CHOICES = {
    (5, '❤️❤️❤️❤️❤️'),
    (4, '💛💛💛💛'),
    (3, '💚💚💚'),
    (2, '💙💙'),
    (1, '💜')
}

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    painting = Base64Field(max_length=900000, blank=True, null=True)
    mood = models.IntegerField(choices=MOOD_CHOICES)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
