# Generated by Django 5.0.2 on 2024-02-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mm_hp', '0004_remove_imagemodel_aligned_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='black_and_white_image',
            field=models.ImageField(blank=True, null=True, upload_to='blackAndWhite/'),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='grayscale_image',
            field=models.ImageField(blank=True, null=True, upload_to='grayscale/'),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='original_image',
            field=models.ImageField(upload_to='original/'),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='resized_image',
            field=models.ImageField(blank=True, null=True, upload_to='resize/'),
        ),
    ]