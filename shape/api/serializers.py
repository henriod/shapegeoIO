from django.contrib.gis.db import models
from django.db.models import fields
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from shape.models import multiPolygonFeatures, multiLinestringFeatures, multiPointFeatures, ShapefileZip
from django.contrib.gis.geos import Polygon


class shapefileSeliazer(serializers.ModelSerializer):

    class Meta:
        model = ShapefileZip
        fields = '__all__'


class polygonSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = multiPolygonFeatures
        fields = ['geo']
        geo_field = 'geo'
        auto_bbox = True

    def get_properties(self, instance, fields):
        # This is a PostgreSQL HStore field, which django maps to a dict
        return instance.medata

    def unformat_geojson(self, feature):
        attrs = {
            self.Meta.geo_field: feature["geometry"],
            "medata": feature["properties"]
        }

        if self.Meta.bbox_geo_field and "bbox" in feature:
            attrs[self.Meta.bbox_geo_field] = Polygon.from_bbox(
                feature["bbox"])

        return attrs


class lineSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = multiLinestringFeatures
        fields = ['geo']
        geo_field = 'geo'
        auto_bbox = True

    def get_properties(self, instance, fields):
        # This is a PostgreSQL HStore field, which django maps to a dict
        return instance.medata

    def unformat_geojson(self, feature):
        attrs = {
            self.Meta.geo_field: feature["geometry"],
            "medata": feature["properties"]
        }

        if self.Meta.bbox_geo_field and "bbox" in feature:
            attrs[self.Meta.bbox_geo_field] = Polygon.from_bbox(
                feature["bbox"])

        return attrs


class pointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = multiPointFeatures
        fields = ['geo']
        geo_field = 'geo'
        auto_bbox = True

    def get_properties(self, instance, fields):
        # This is a PostgreSQL HStore field, which django maps to a dict
        return instance.medata

    def unformat_geojson(self, feature):
        attrs = {
            self.Meta.geo_field: feature["geometry"],
            "medata": feature["properties"]
        }

        if self.Meta.bbox_geo_field and "bbox" in feature:
            attrs[self.Meta.bbox_geo_field] = Polygon.from_bbox(
                feature["bbox"])

        return attrs
