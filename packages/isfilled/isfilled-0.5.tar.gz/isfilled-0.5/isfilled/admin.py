from django.conf import settings
from django.contrib import admin

from isfilled.models import Fill

class FillAdmin(admin.ModelAdmin):
    list_display = ['name', 'fill', 'model', 'form',]

admin.site.register(Fill, FillAdmin)
