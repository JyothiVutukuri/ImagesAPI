from django.core.exceptions import ValidationError
from django.db import models


class Image(models.Model):
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def clean(self):
        if not self.title and not self.description and not self.url:
            raise ValidationError("All fields cannot be blank")


