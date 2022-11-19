from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_lengt  = 256)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering= ['-publish']
        index = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self):
        return self.title

    