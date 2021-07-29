from django.db import router
from rest_framework.routers import DefaultRouter
from shape.api.views import shapefileViewSet


router = DefaultRouter()
router.register(r'shapefiles', shapefileViewSet, basename='shapefiles')

urlpatterns = router.urls