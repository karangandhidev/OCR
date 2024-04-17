from django.urls import path
from . import views
from OCR import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.get_form, name ='create'),
    # path('pdf', views.ocrtest, name = 'pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)