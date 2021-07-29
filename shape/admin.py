from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import ShapefileZip, multiPolygonFeatures, multiLinestringFeatures, multiPointFeatures
# Register your models here.

admin.site.register(ShapefileZip)
admin.site.register(multiPointFeatures)
admin.site.register(multiLinestringFeatures)
admin.site.register(multiPolygonFeatures)