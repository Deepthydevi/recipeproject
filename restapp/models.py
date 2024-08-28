from datetime import timedelta

from django.db import models

# Create your models here.
class Recipes(models.Model):
    Name=models.CharField(max_length=250)
    Pre_time=models.DurationField(default=timedelta(minutes=120))
    DIFFICULTY_CHOICES=[
        (1,'Easy'),
        (2,'Medium'),
        (3,'Hard')
    ]
    Difficulty=models.IntegerField(choices=DIFFICULTY_CHOICES)
    Vegetarian=models.BooleanField()
    Recipe_img=models.ImageField(upload_to='recipe')
    Description=models.CharField(max_length=500)
