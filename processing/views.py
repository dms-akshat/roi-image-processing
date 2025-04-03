import os
import zipfile
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .image_processing import process_image

def home(request):
    return render(request, 'home.html')

def upload(request):
    return render(request, 'upload.html')

def process_single(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT + "/uploads/")
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url("uploads/" + filename)
        
        processed_image_path, score = process_image(os.path.join(settings.MEDIA_ROOT, "uploads", filename))
        
        return render(request, 'result.html', {
            'original_image': uploaded_file_url,
            'processed_image': settings.MEDIA_URL + "processed/" + filename,
            'similarity_score': score,
        })
    
    return redirect('upload')

def process_folder(request):
    if request.method == 'POST' and request.FILES.getlist('folder'):
        folder = request.FILES.getlist('folder')
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "uploads"))
        processed_images = []

        for image in folder:
            filename = fs.save(image.name, image)
            uploaded_file_url = settings.MEDIA_URL + "uploads/" + filename
            processed_image_path, score = process_image(os.path.join(settings.MEDIA_ROOT, "uploads", filename))

            processed_images.append({
                'original': uploaded_file_url,
                'processed': settings.MEDIA_URL + "processed/" + os.path.basename(processed_image_path),
                'similarity_score': score
            })

        return render(request, 'result.html', {'images': processed_images})
    
    return redirect('upload')


def results(request):
    return render(request, 'result.html')
