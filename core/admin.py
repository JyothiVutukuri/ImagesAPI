from django.contrib import admin
from core.models import Image
from import_export.admin import ImportMixin
from import_export import resources
from import_export.fields import Field


class ImageResource(resources.ModelResource):
    id = Field(attribute='id')
    title = Field(attribute='title')
    description = Field(attribute='description')
    image = Field(attribute='url')

    class Meta:
        model = Image
        fields = ('id', 'title', 'description', 'image')
        import_order = fields


@admin.register(Image)
class ImageAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ["title", "description", "url"]
    search_fields = ["title"]

    resource_class = ImageResource

