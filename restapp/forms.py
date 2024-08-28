from django import forms
from .models import Recipes

class RecipesForm(forms.ModelForm):
    Pre_time = forms.DurationField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration as HH:MM:SS'}),
        help_text='Duration in HH:MM:SS or days, hours:minutes:seconds format'
    )

    class Meta:
        model = Recipes
        fields = '__all__'
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Difficulty': forms.Select(attrs={'class': 'form-control'}),
            'Vegetarian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Description': forms.Textarea(attrs={'class': 'form-control'}),
            'Recipe_img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
