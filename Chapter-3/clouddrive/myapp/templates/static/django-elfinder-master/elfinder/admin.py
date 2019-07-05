from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import File, Directory, FileCollection

admin.site.register(Directory, MPTTModelAdmin)
admin.site.register(FileCollection)
admin.site.register(File)
