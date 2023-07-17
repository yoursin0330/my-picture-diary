from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
MOOD_CHOICES = {
    (5,'❤️❤️❤️❤️❤️'),
    (4,'💛💛💛💛'),
    (3,'💚💚💚' ),
    (2,'💙💙'),
    (1,'💜')
}

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # picture = models.ImageField(upload_to=None, height_field=400, width_field=400, null=True)
    mood = models.IntegerField(choices=MOOD_CHOICES)
    


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
