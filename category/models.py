# <category의 models.py>
from django.db import models
import os

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'