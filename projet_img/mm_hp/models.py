from django.db import models

class ImageModel(models.Model):
    original_image = models.ImageField(upload_to='original/')  # Mettez 'original/' au lieu de 'images/original/'
    black_and_white_image = models.ImageField(upload_to='blackAndWhite/', blank=True, null=True)
    resized_image = models.ImageField(upload_to='resize/', blank=True, null=True)
    grayscale_image = models.ImageField(upload_to='grayscale/', blank=True, null=True)
