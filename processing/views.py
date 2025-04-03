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
        
        # ✅ Store processed images in session for ZIP download
        request.session['processed_images'] = [img['processed'] for img in processed_images]
        request.session.modified = True

        return render(request, 'result.html', {'images': processed_images})
    
    return redirect('upload')

import io
from django.http import HttpResponse

def download_processed_images(request):
    # ✅ Retrieve processed images from session
    processed_images = request.session.get('processed_images', [])

    if not processed_images:
        return HttpResponse("No processed images found.", status=404)

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for img_url in processed_images:
            # Convert URL to absolute file path
            img_path = os.path.join(settings.MEDIA_ROOT, img_url.replace(settings.MEDIA_URL, ""))

            # Ensure file exists before adding to ZIP
            if os.path.exists(img_path):
                zip_file.write(img_path, os.path.basename(img_path))
            else:
                print(f"⚠️ File not found: {img_path}")  # Debugging line

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=processed_images.zip"
    return response


def results(request):
    return render(request, 'result.html')
