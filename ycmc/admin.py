from django.contrib import admin
from .models import DetectInformation


# Register your models here.
@admin.register(DetectInformation)
class DetectInformation(admin.ModelAdmin):
    list_display = ['_id','repo1','repo2','data','date']
    