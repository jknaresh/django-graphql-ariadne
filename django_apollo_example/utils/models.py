from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    class Meta:
        abstract = True
        ordering = ("-u_on",)

    # row alpha numeric slug
    slug = models.SlugField(
        default=uuid4, unique=True, help_text=_("row id"), editable=False
    )

    # status of record
    is_active = models.PositiveSmallIntegerField(default=0, verbose_name="active row")

    status = models.PositiveIntegerField(default=0, verbose_name=_("row status"))

    # record created on
    c_on = models.DateTimeField(auto_now_add=True, verbose_name="created on")
    # record updated on
    u_on = models.DateTimeField(auto_now=True, verbose_name="updated on")

    def __str__(self):
        return f"{self.slug}"

    @classmethod
    def get_queryset(cls, **kwargs):
        return cls.objects.filter(**kwargs)
