#models.py

from django.db import models
from django.db import models
from django.db.models import permalink
from ckeditor.fields import RichTextField


class Policy(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = RichTextField(max_length=250)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return  self.title




