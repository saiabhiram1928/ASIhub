from django.contrib import admin
from . import models

admin.site.register(models.Room)
admin.site.register(models.Messages)
admin.site.register(models.Topic)
admin.site.register(models.Profile)

# Register your models here.

