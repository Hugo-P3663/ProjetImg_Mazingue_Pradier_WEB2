from django.db import models

class ImageModel(models.Model):
    original_image = models.ImageField(upload_to='images/original/')
    black_and_white_image = models.ImageField(upload_to='images/blackAndWhite/', blank=True, null=True)
    resized_image = models.ImageField(upload_to='images/resize/', blank=True, null=True)
    grayscale_image = models.ImageField(upload_to='images/grayscale/', blank=True, null=True)
    #aligned_image = models.ImageField(upload_to='images/aligned/', blank=True, null=True)
    #merged_image = models.ImageField(upload_to='images/merged/', blank=True, null=True)
    #animated_image = models.ImageField(upload_to='images/animated/', blank=True, null=True)