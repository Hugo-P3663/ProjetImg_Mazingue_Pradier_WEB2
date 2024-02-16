from django import forms
from .models import ImageModel

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['original_image1', 'original_image2']