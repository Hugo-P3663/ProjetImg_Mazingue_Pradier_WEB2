from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import ImageModel
from PIL import Image, ImageFilter
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.conf import settings
import os

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('process_image', image_id=instance.id)
    else:
        form = ImageForm()

    # Récupérer les images dans l'ordre inverse d'importation
    images = ImageModel.objects.all().order_by('-id')  # L'ordre décroissant des ID garantit que les dernières images sont affichées en premier

    return render(request, 'home.html', {'form': form, 'images': images})


def process_image(request, image_id):
    image = ImageModel.objects.get(pk=image_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'convert_bw':
            apply_black_and_white(image)
        elif action == 'apply_filter':
            filter_type = request.POST.get('filter_type')
            apply_grayscale_filter(image, filter_type)
        elif action == 'resize':
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))
            apply_resize(image, width, height)

        # Recharger l'objet image pour obtenir les chemins des images modifiées
        image.refresh_from_db()

    return render(request, 'process_image.html', {'image': image})

def apply_black_and_white(image_obj):
    with open(image_obj.original_image.path, 'rb') as f:
        original_image = Image.open(f)
        black_and_white_image = original_image.convert('L')

        # Construire le chemin de destination pour l'image en noir et blanc
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'bw')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original
        original_image_name = os.path.basename(image_obj.original_image.name)

        # Construire le chemin complet du fichier en noir et blanc
        black_and_white_image_path = os.path.join(destination_dir, 'bw_' + original_image_name)

        # Enregistrer l'image en noir et blanc
        black_and_white_image.save(black_and_white_image_path)

        # Enregistrer le chemin de l'image en noir et blanc dans le modèle
        image_obj.black_and_white_image = 'bw/bw_' + original_image_name
        image_obj.save()


def apply_resize(image, width, height):
    img = Image.open(image.original_image.path)
    resized_image = img.resize((width, height))

    # Construire le chemin de destination pour l'image redimensionnée
    destination_dir = os.path.join(settings.MEDIA_ROOT, 'resized')
    os.makedirs(destination_dir, exist_ok=True)

    # Extraire le nom du fichier original
    original_image_name = os.path.basename(image.original_image.name)

    # Construire le chemin complet du fichier redimensionné
    resized_image_path = os.path.join(destination_dir, 'resized_' + original_image_name)

    # Enregistrer l'image redimensionnée
    resized_image.save(resized_image_path)

    # Enregistrer le chemin de l'image redimensionnée dans le modèle
    image.resized_image = 'resized/resized_' + original_image_name
    image.save()

def apply_grayscale_filter(image_obj, filter_type):
    with open(image_obj.original_image.path, 'rb') as f:
        original_image = Image.open(f)
        grayscale_image = nuance_de_gris(original_image, ImageFilter.SHARPEN)

        # Construire le chemin de destination pour l'image en nuances de gris
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'grayscale')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original
        original_image_name = os.path.basename(image_obj.original_image.name)

        # Construire le chemin complet du fichier en nuances de gris
        grayscale_image_path = os.path.join(destination_dir, 'grayscale_' + original_image_name)

        # Enregistrer l'image en nuances de gris
        grayscale_image.save(grayscale_image_path)

        # Enregistrer le chemin de l'image en nuances de gris dans le modèle
        image_obj.grayscale_image = 'grayscale/grayscale_' + original_image_name
        image_obj.save()

def nuance_de_gris(image, filtre):
    return image.convert("L", palette=Image.ADAPTIVE, colors=256).filter(filtre)