from distutils.text_file import TextFile
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from django.conf import settings

class Tags(models.Model):
    taste = models.IntegerField(default=0)
    interior = models.IntegerField(default=0)
    dessert = models.IntegerField(default=0)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

class Cafe(models.Model):
    name = models.CharField(max_length=20)
    hits = models.IntegerField(default=0)
    adress = models.CharField(max_length=50)
    telephone = models.TextField()
    opening = models.TextField()
    lastorder = models.TimeField()
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

