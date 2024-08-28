from .models import *
from rest_framework import serializers

class RecipesSerializers(serializers.ModelSerializer):
    Recipe_img=serializers.ImageField(required=False)
    
    class Meta:
        model=Recipes
        fields='__all__'