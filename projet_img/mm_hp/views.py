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

    images = ImageModel.objects.all().order_by('-id')
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
        elif action == 'merge':
            rate = float(request.POST.get('rate'))
            merge_images(image, rate)
        elif action == 'alignment':
            alignment_type = str(request.POST.get('alignment_type'))
            apply_alignment(image, alignment_type)

        # Rafraîchir les données de l'objet image depuis la base de données après les modifications
        image.refresh_from_db()

    # Envoyer le contexte mis à jour au template
    return render(request, 'process_image.html', {'image': image, 'form': ImageForm()})


def apply_black_and_white(image_obj):
    with open(image_obj.original_image1.path, 'rb') as f1, open(image_obj.original_image2.path, 'rb') as f2:
        original_image1 = Image.open(f1)
        original_image2 = Image.open(f2)

        # Convertir les deux images en noir et blanc
        black_and_white_image1 = original_image1.convert("1")
        black_and_white_image2 = original_image2.convert("1")

        # Construire le chemin de destination pour les images en noir et blanc
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'bw')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original pour les deux images
        original_image1_name = os.path.basename(image_obj.original_image1.name)
        original_image2_name = os.path.basename(image_obj.original_image2.name)

        # Construire les chemins complets pour les images en noir et blanc
        black_and_white_image1_path = os.path.join(destination_dir, 'bw_' + original_image1_name)
        black_and_white_image2_path = os.path.join(destination_dir, 'bw_' + original_image2_name)

        # Enregistrer les images en noir et blanc
        black_and_white_image1.save(black_and_white_image1_path)
        black_and_white_image2.save(black_and_white_image2_path)

        # Enregistrer les chemins des images en noir et blanc dans le modèle
        image_obj.black_and_white_image1 = 'bw/bw_' + original_image1_name
        image_obj.black_and_white_image2 = 'bw/bw_' + original_image2_name
        image_obj.save()

def apply_resize(image_obj, width, height):
    with open(image_obj.original_image1.path, 'rb') as f1, open(image_obj.original_image2.path, 'rb') as f2:
        original_image1 = Image.open(f1)
        original_image2 = Image.open(f2)

        # Redimensionner les deux images
        resized_image1 = original_image1.resize((width, height))
        resized_image2 = original_image2.resize((width, height))

        # Construire le chemin de destination pour les images redimensionnées
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'resized')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original pour les deux images
        original_image1_name = os.path.basename(image_obj.original_image1.name)
        original_image2_name = os.path.basename(image_obj.original_image2.name)

        # Construire les chemins complets pour les images redimensionnées
        resized_image1_path = os.path.join(destination_dir, 'resized_' + original_image1_name)
        resized_image2_path = os.path.join(destination_dir, 'resized_' + original_image2_name)

        # Enregistrer les images redimensionnées
        resized_image1.save(resized_image1_path)
        resized_image2.save(resized_image2_path)

        # Enregistrer les chemins des images redimensionnées dans le modèle
        image_obj.resized_image1 = 'resized/' + os.path.basename(resized_image1_path)
        image_obj.resized_image2 = 'resized/' + os.path.basename(resized_image2_path)
        image_obj.save()


def apply_grayscale_filter(image_obj, filter_type):
    with open(image_obj.original_image1.path, 'rb') as f1, open(image_obj.original_image2.path, 'rb') as f2:
        original_image1 = Image.open(f1)
        original_image2 = Image.open(f2)

        # Appliquer un filtre de couleur à l'image
        if filter_type == 'BLUR':
            grayscale_image1 = original_image1.filter(ImageFilter.BLUR)
            grayscale_image2 = original_image2.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            grayscale_image1 = original_image1.filter(ImageFilter.CONTOUR)
            grayscale_image2 = original_image2.filter(ImageFilter.CONTOUR)
        elif filter_type == 'DETAIL':
            grayscale_image1 = original_image1.filter(ImageFilter.DETAIL)
            grayscale_image2 = original_image2.filter(ImageFilter.DETAIL)
        elif filter_type == 'EDGE_ENHANCE':
            grayscale_image1 = original_image1.filter(ImageFilter.EDGE_ENHANCE)
            grayscale_image2 = original_image2.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'EMBOSS':
            grayscale_image1 = original_image1.filter(ImageFilter.EMBOSS)
            grayscale_image2 = original_image2.filter(ImageFilter.EMBOSS)
        elif filter_type == 'FIND_EDGES':
            grayscale_image1 = original_image1.filter(ImageFilter.FIND_EDGES)
            grayscale_image2 = original_image2.filter(ImageFilter.FIND_EDGES)
        elif filter_type == 'SHARPEN':
            grayscale_image1 = original_image1.filter(ImageFilter.SHARPEN)
            grayscale_image2 = original_image2.filter(ImageFilter.SHARPEN)
        else:
            grayscale_image1 = original_image1
            grayscale_image2 = original_image2

        # Construire le chemin de destination pour les images en niveaux de gris
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'grayscale')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original pour les deux images
        original_image1_name = os.path.basename(image_obj.original_image1.name)
        original_image2_name = os.path.basename(image_obj.original_image2.name)

        # Construire les chemins complets pour les images en niveaux de gris
        grayscale_image1_path = os.path.join(destination_dir, 'grayscale_' + original_image1_name)

        grayscale_image2_path = os.path.join(destination_dir, 'grayscale_' + original_image2_name)

        # Enregistrer les images en niveaux de gris
        grayscale_image1.save(grayscale_image1_path)
        grayscale_image2.save(grayscale_image2_path)

        # Enregistrer les chemins des images en niveaux de gris dans le modèle
        image_obj.grayscale_image1 = 'grayscale/grayscale_' + original_image1_name
        image_obj.grayscale_image2 = 'grayscale/grayscale_' + original_image2_name
        image_obj.save()

def merge_images(image_obj, rate):
    with open(image_obj.original_image1.path, 'rb') as f1, open(image_obj.original_image2.path, 'rb') as f2:
        original_image1 = Image.open(f1)
        original_image2 = Image.open(f2)

        # Resize the second image to match the size of the first image
        original_image2 = original_image2.resize(original_image1.size)

        # Blend the two images
        merged_image = Image.blend(original_image1, original_image2, alpha=rate)

        # Build the destination path for the merged image
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'merged')
        os.makedirs(destination_dir, exist_ok=True)

        original_image1_name = os.path.basename(image_obj.original_image1.name)
        original_image2_name = os.path.basename(image_obj.original_image2.name)

        merged_image_path = os.path.join(destination_dir, 'merged_' + original_image1_name + '_' + original_image2_name)

        # Save the merged image
        merged_image.save(merged_image_path)

        # Save the path of the merged image in the model
        image_obj.merged_image = 'merged/merged_' + original_image1_name + '_' + original_image2_name
        image_obj.save()
        
        
        
def apply_alignment(image_obj, direction):
    with open(image_obj.original_image1.path, 'rb') as f1, open(image_obj.original_image2.path, 'rb') as f2:
        original_image1 = Image.open(f1)
        original_image2 = Image.open(f2)

        if direction == "VERTICAL":
            if original_image1.width != original_image2.width:
                original_image2 = original_image2.resize((original_image1.width, original_image2.height))
                
            total_width = max(original_image1.width, original_image2.width)
            total_height = original_image1.height + original_image2.height
            alignment_image = Image.new('RGB', (total_width, total_height), "white")
            alignment_image.paste(original_image1, (0, 0))
            alignment_image.paste(original_image2, (0, original_image1.height))
            
        elif direction == "HORIZONTAL":
            if original_image1.height != original_image2.height:
                original_image2 = original_image2.resize((original_image2.width, original_image1.height))
                
            total_width = original_image1.width + original_image2.width
            total_height = max(original_image1.height, original_image2.height)
            alignment_image = Image.new('RGB', (total_width, total_height), "white")
            alignment_image.paste(original_image1, (0, 0))
            alignment_image.paste(original_image2, (original_image1.width, 0))
        
        # Construire le chemin de destination pour l'alignement des deux images
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'alignment')
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original
        original_image1_name = os.path.basename(image_obj.original_image1.name)

        # Construire le chemin complet du fichier aligné
        alignment_image_path = os.path.join(destination_dir, 'alignment_' + original_image1_name)

        # Enregistrer l'image aligné
        alignment_image.save(alignment_image_path)

        # Enregistrer le chemin de l'image aligné dans le modèle
        image_obj.alignment_image = 'alignment/alignment_' + original_image1_name
        image_obj.save()