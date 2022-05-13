from numpy import nan
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from core.models import Image
from core.serializers import ImageSerializer, ImageUploadSerializer
import pandas as pd


class UploadImagesView(CreateAPIView):
    serializer_class = ImageUploadSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images_file_link = serializer.validated_data['images_file_link']
        new_images = []
        try:
            chunk = pd.read_csv(images_file_link, na_filter=False, chunksize=10000)
            reader = pd.concat(chunk)
            for _, row in reader.iterrows():
                title = row["title"]
                description = row["description"]
                image = row["image"]
                if title or description or image:
                    new_images.append(Image(title=title, description=description, url=image))
            if not new_images:
                return Response({"status": "empty csv / all null values"}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "invalid csv"}, status.HTTP_400_BAD_REQUEST)

        Image.objects.bulk_create(new_images)
        return Response({"status": "success"}, status.HTTP_201_CREATED)


class ImagesView(ListModelMixin, GenericViewSet):
    """
    API endpoint that gives list of all images.
    """
    queryset = Image.objects.all().order_by('id')
    serializer_class = ImageSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ImageView(RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that gives single image instance.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # permission_classes = [permissions.IsAuthenticated]





