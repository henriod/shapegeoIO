import os
import glob
import zipfile
import shutil
import traceback

from osgeo import ogr, osr

from django.contrib.gis.db import models
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.gis.geos.collections import MultiLineString, MultiPoint, MultiPolygon
from django.contrib.postgres.fields import HStoreField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class ShapefileZip(models.Model):
    file = models.FileField(upload_to='shp')
    filename = models.CharField(max_length=255)
    srs_wkt = models.CharField(max_length=255)
    geom_type = models.CharField(max_length=55)

    def __str__(self):
        return self.filename

class multiPointFeatures(models.Model):
    shapefile = models.ForeignKey(ShapefileZip, on_delete=models.CASCADE)
    medata = HStoreField(blank=True, null=True, default=dict)
    geo = models.MultiPointField(srid=4326)

class multiLinestringFeatures(models.Model):
    shapefile = models.ForeignKey(ShapefileZip, on_delete=models.CASCADE)
    medata = HStoreField(blank=True, null=True, default=dict)
    geo = models.MultiLineStringField(srid=4326)

class multiPolygonFeatures(models.Model):
    shapefile = models.ForeignKey(ShapefileZip, on_delete=models.CASCADE)
    medata = HStoreField(blank=True, null=True, default=dict)
    geo = models.MultiPolygonField(srid=4326)


@receiver(post_save, sender=ShapefileZip)
def poblish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_path = os.path.dirname(file)
    
    if not zipfile.is_zipfile(file):
        return "File not a valid zipfile."

    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove(file)

    #we get the shapefile from the extracted zip file
    shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=True)[0]
       
    #using ogr to interact with the shapefile
    try:
        datasource = ogr.Open(shp)
        layer = datasource.GetLayer(0)
        shapefile_ok = True
    except:
        traceback.print_exc()
        shapefile_ok = False

    if not shapefile_ok:
        return "Not a valid shapefile."

    #source spatial reference system
    src_spatail_ref = layer.GetSpatialRef()
    geom_type = layer.GetLayerDefn().GetGeomType()
    geom_name = ogr.GeometryTypeToName(geom_type)

    #destination spatial reference system
    dst_spatial_ref = osr.SpatialReference()
    dst_spatial_ref.ImportFromEPSG(4326)
    coord_transform = osr.CoordinateTransformation(src_spatail_ref, dst_spatial_ref)
    '''
    creating array to store attribute labels of the features
    '''
    attributes = []
    layer_def = layer.GetLayerDefn()
    for i in range(layer_def.GetFieldCount()):
        field_def = layer_def.GetFieldDefn(i)
        name = field_def.GetName()
        attributes.append(name)

    for i in range(layer.GetFeatureCount()):
        src_feature = layer.GetFeature(i)
        src_geometry = src_feature.GetGeometryRef()
        '''
        check if there is a feature missing geometry
        '''
        if src_geometry != None: 
            '''
            Check if the source and destination spatial ref are eqaul before transformation
            helps prevent coordinate reversing
            '''
            if str(src_spatail_ref) != str(dst_spatial_ref):                  
                src_geometry.Transform(coord_transform)
                print('hello amd not equal')
                
            geometry = GEOSGeometry(src_geometry.ExportToWkt())
            '''
            Creating a dictionary to store feature attribute information
            '''
            metadata ={}
            for attr in attributes:
                value = src_feature.GetFieldAsString(attr)
                metadata[str(attr)] = str(value)
            '''
            checking for feature geometry type and choosing appropriate model to store it
            '''
            if geom_name == 'Point':
                geometry = MultiPoint(geometry)
                points = multiPointFeatures(
                    shapefile = instance,
                    medata = metadata,
                    geo = geometry
                )
                points.save()
            elif geom_name == 'LineString':
                geometry = MultiLineString(geometry)
                lines = multiLinestringFeatures(
                    shapefile = instance,
                    medata = metadata,
                    geo = geometry
                )
                lines.save()
            elif geom_name == 'Polygon':
                geometry = MultiPolygon(geometry)
                polygons = multiPolygonFeatures(
                    shapefile = instance,
                    medata = metadata,
                    geo = geometry
                )
                polygons.save()
            else:
                return "Feature geomtry is undefined"
    #cleaning up the directory 
    shutil.rmtree(file_path)