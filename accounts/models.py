from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class User(AbstractUser):

    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    area = models.CharField(max_length=50, default='서울')
    profile_image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(360, 360)],
                                format='JPEG',
                                options={'quality': 80})
    taste = models.IntegerField(default=0)
    interior = models.IntegerField(default=0)
    dessert = models.IntegerField(default=0)