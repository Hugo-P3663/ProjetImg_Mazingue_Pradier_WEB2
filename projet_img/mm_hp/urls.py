from django.urls import path
from .views import home

from django.urls import path
from .views import home, process_image

urlpatterns = [
    path('', home, name='home'),
    path('process_image/<int:image_id>/', process_image, name='process_image'),
    # Autres URLs...
]