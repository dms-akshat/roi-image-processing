from django.urls import path
from .views import home, upload, process_single, process_folder, results, download_processed_images

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('process_single/', process_single, name='process_single'),
    path('process_folder/', process_folder, name='process_folder'),
    path("download-zip/", download_processed_images, name="download_zip"),
    path('results/', results, name='results'),
]
