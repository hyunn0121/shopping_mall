from django.db import models

# Create your models here.

class Manufacturer(models.Model):
    company = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    email = models.CharField(max_length=30)

    # slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.company

    def get_absolute_url(self):
        return f'/product/manufacturer/{self.slug}/'