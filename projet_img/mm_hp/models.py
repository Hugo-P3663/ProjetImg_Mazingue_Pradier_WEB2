from django.db import models

class ImageModel(models.Model):
    original_image1 = models.ImageField(upload_to='original/')
    original_image2 = models.ImageField(upload_to='original/')
    black_and_white_image1 = models.ImageField(upload_to='blackAndWhite/', blank=True, null=True)
    black_and_white_image2 = models.ImageField(upload_to='blackAndWhite/', blank=True, null=True)
    resized_image1 = models.ImageField(upload_to='resized/', blank=True, null=True)
    resized_image2 = models.ImageField(upload_to='resized/', blank=True, null=True)
    grayscale_image1 = models.ImageField(upload_to='grayscale/', blank=True, null=True)
    grayscale_image2 = models.ImageField(upload_to='grayscale/', blank=True, null=True)
    merged_image = models.ImageField(upload_to='merged/', blank=True, null=True)
    alignment_image = models.ImageField(upload_to='alignment/', blank=True, null=True)
