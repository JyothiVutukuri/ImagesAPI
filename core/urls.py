from django.contrib import admin

from django.urls import include, path
from rest_framework import routers

from core.views import ImageView, ImagesView, UploadImagesView

app_name = "core"

router = routers.DefaultRouter()
router.register(r'images', ImagesView, basename='images')
router.register(r'image', ImageView, basename='image')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-images/', UploadImagesView.as_view(), name='upload_images')
]