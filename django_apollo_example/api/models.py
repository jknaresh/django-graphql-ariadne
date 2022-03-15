from django.db import models

from utils.models import AbstractModel


class Post(AbstractModel):
    title = models.CharField(max_length=15, null=True)
    description = models.TextField(null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "c_on": str(self.c_on.strftime("%d-%m-%Y")),
        }
