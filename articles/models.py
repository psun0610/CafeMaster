from distutils.text_file import TextFile
from random import choices
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from multiselectfield import MultiSelectField
from django.db import models
from django.conf import settings

good = (
    (1,'커피맛'),
    (2,'인테리어'),
    (3,'디저트'),
)


class Cafe(models.Model):
    name = models.CharField(max_length=20)
    hits = models.IntegerField(default=0)
    adress = models.CharField(max_length=50)
    telephone = models.TextField()
    opening = models.TextField()
    lastorder = models.TimeField()
    #해시태그
    taste = models.IntegerField(default=0)
    interior = models.IntegerField(default=0)
    dessert = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    tag = MultiSelectField(choices=good, max_choices=6)


