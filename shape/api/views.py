from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination
from .serializers import shapefileSeliazer, polygonSerializer, pointSerializer, lineSerializer
from shape.models import ShapefileZip

# Create your views here.


class shapefileViewSet(viewsets.ModelViewSet):
    queryset = ShapefileZip.objects.all()
    serializer_class = shapefileSeliazer

    @action(detail=True)
    def points(self, request, pk=None):
        """
        Map of the registered parcel
        """
        shp = self.get_object()
        points = shp.multipointfeatures_set.all()
        '''
        pagination of the geojson to reduce loading time
        '''
        paginator = GeoJsonPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(points, request)
        if page is not None:
            serializer = pointSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = pointSerializer(data=points, many=True)
        serializer.is_valid()

        return Response(serializer.data)

    @action(detail=True)
    def lines(self, request, pk=None):
        """
        Map of the registered parcel
        """
        shp = self.get_object()
        lines = shp.multilinestringfeatures_set.all()
        '''
        pagination of the geojson to reduce loading time
        '''
        paginator = GeoJsonPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(lines, request)
        if page is not None:
            serializer = lineSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = lineSerializer(data=lines, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    @action(detail=True)
    def plygons(self, request, pk=None):
        """
        Map of the registered parcel
        """
        shp = self.get_object()
        polygons = shp.multipolygonfeatures_set.all()
        '''
        pagination of the geojson to reduce loading time
        '''
        paginator = GeoJsonPagination()
        paginator.page_size = 100
        page = paginator.paginate_queryset(polygons, request)
        if page is not None:
            serializer = polygonSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = polygonSerializer(data=polygons, many=True)
        serializer.is_valid()
        return Response(serializer.data)

