from django.db import models
from django.utils.translation import gettext_lazy as _


class SimulateContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(_('python model class name'), max_length=100)


class SimulatePermission(models.Model):
    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        SimulateContentType,
        models.CASCADE,
        verbose_name=_('content type'),
        related_name="sp_set",
        related_query_name="sp"
    )
    codename = models.CharField(_('codename'), max_length=100)
