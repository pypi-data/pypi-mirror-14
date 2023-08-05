# -*- coding: utf-8 -*-
from django.apps import apps
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.db.models import Count

from isfilled.util import import_string

class Fill(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    fill = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    model = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    fields = models.CharField(max_length=255, null=True, blank=True)
    exclude = models.CharField(max_length=255, null=True, blank=True)

    def fill_model(self):
        fills = import_string(self.fill)
        return fills.form.Meta.model

    def model_model(self):
        return apps.get_model(self.model)

    def save(self, *args, **kwargs):
        if self.fill and not self.model:
            model = self.fill_model()
            self.model = model._meta.label
        super(Fill, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'fill', 'model'),)

