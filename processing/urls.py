from django.urls import path
from .views import home, upload, process_single, process_folder, results

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('process_single/', process_single, name='process_single'),
    path('process_folder/', process_folder, name='process_folder'),
    path('results/', results, name='results'),
]
