# -*- coding: utf-8 -*-
from django.apps import apps
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.db.models import Count

from isfilled.util import import_string

class Fill(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, db_index=True)
    fill = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    model = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    form = models.CharField(max_length=255, null=True, blank=True)
    fields = models.CharField(max_length=255, null=True, blank=True)
    exclude = models.CharField(max_length=255, null=True, blank=True)

    def str_as_list(self, fld):
        return filter(None, (getattr(self, fld) or '').split(','))

    def fill_model(self):
        fills = import_string(self.fill)
        return fills.form.Meta.model

    def form_model(self):
        return self.using_form().Meta.model

    def using_form(self):
        return import_string(self.form)

    def model_model(self):
        return apps.get_model(self.model)

    def save(self, *args, **kwargs):
        if self.fill and not self.model:
            self.model = self.fill_model()._meta.label
        if self.form and not self.model:
            self.model = self.form_model()._meta.label
        super(Fill, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
