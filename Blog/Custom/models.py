from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from django.db.models.fields import TextField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=500, null=False)
    #description = RichTextField()
    description = TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @property
    def is_modified(self):
        return self.publish_date < self.update_date

    def __str__(self):
        return self.title