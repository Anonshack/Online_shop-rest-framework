from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Shop(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self) -> str:
         return self.name

class Clothing(models.Model):
    menu = models.ForeignKey(Shop, on_delete=models.CASCADE)  
    name = models.CharField(max_length=155, verbose_name='Name')
    info = models.TextField(verbose_name='Information')
    price = models.IntegerField(verbose_name='Price')
    year = models.IntegerField(verbose_name='Year')
    image = models.URLField(verbose_name='URL field')
    set_data = models.DateField()

    EFFECTS_CHOICES = [
        ('g', 'good'),
        ('v', 'very good'),
        ('i', 'interesting'),
    ]

    effects = models.CharField(
        max_length=15,
        verbose_name='Effects',
        choices=EFFECTS_CHOICES,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author',
        default=None,
    )

    def __str__(self):
        return self.name


class AboutPage(models.Model):
      title = models.CharField(max_length=155)
      image = models.ImageField(upload_to='about/', verbose_name='Images')
      info = models.TimeField(verbose_name='About Us')

      def __str__(self) -> str:
            return self.title
