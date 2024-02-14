from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import ImageModel
from PIL import Image, ImageFilter

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('process_image', image_id=instance.id)
    else:
        form = ImageForm()

    images = ImageModel.objects.all()
    return render(request, 'home.html', {'form': form, 'images': images})

def process_image(request, image_id):
    image = ImageModel.objects.get(pk=image_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'convert_bw':
            apply_black_and_white(image)
        elif action == 'resize':
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))
            apply_resize(image, width, height)

        # Recharger l'objet image pour obtenir les chemins des images modifiées
        image.refresh_from_db()

    return render(request, 'process_image.html', {'image': image})


import os

def apply_black_and_white(image_obj):
    # Ouvrir l'image
    with open(image_obj.original_image.path, 'rb') as f:
        original_image = Image.open(f)

        # Convertir l'image en noir et blanc
        black_and_white_image = original_image.convert('L')

        # Créer le répertoire de destination s'il n'existe pas
        destination_dir = 'images/bw'
        os.makedirs(destination_dir, exist_ok=True)

        # Extraire le nom du fichier original
        original_image_name = os.path.basename(image_obj.original_image.name)

        # Construire le chemin de destination pour l'image en noir et blanc
        black_and_white_image_path = os.path.join(destination_dir, 'bw_' + original_image_name)

        # Enregistrer l'image en noir et blanc
        black_and_white_image.save(black_and_white_image_path)

        # Enregistrer le chemin de l'image en noir et blanc dans le modèle
        image_obj.black_and_white_image = black_and_white_image_path
        image_obj.save()


import os

def apply_resize(image, width, height):
    image_path = image.original_image.path
    img = Image.open(image_path)
    resized_image = img.resize((width, height))

    # Créer le répertoire de destination s'il n'existe pas
    destination_dir = 'images/resized'
    os.makedirs(destination_dir, exist_ok=True)

    # Extraire le nom du fichier original
    original_image_name = os.path.basename(image.original_image.name)

    # Construire le chemin de destination pour l'image redimensionnée
    resized_image_path = os.path.join(destination_dir, 'resized_' + original_image_name)

    # Enregistrer l'image redimensionnée
    resized_image.save(resized_image_path)

    # Enregistrer le chemin de l'image redimensionnée dans le modèle
    image.resized_image = resized_image_path
    image.save()
