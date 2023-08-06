from django.contrib import admin
from . import models

@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display  = [ 'slug', 'updated' ]
    search_fields = [ 'slug' ]
