from django.db import models

class ImageModel(models.Model):
    original_image = models.ImageField(upload_to='images/original/')
    black_and_white_image = models.ImageField(upload_to='images/blackAndWhite/', blank=True, null=True)
    resized_image = models.ImageField(upload_to='images/resize/', blank=True, null=True)