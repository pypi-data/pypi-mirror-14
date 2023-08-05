#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import errno, makedirs
from chardet import detect

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def read_exif(filename):
    """Returns a dict of EXIF tags and values read from the given filename."""
    get, raw = TAGS.get, Image.open(filename)._getexif()
    exif = dict((get(tag, tag), value) for tag, value in raw.items())
    encoding = 'utf8'
    strs = [(k, v) for k, v in exif.items() if isinstance(v, (basestring, ))]
    for key, value in strs:
        try:
            snif = detect(value)
            if snif['confidence'] >= 0.5 and encoding != snif['encoding']:
                encoding = snif['encoding']
            value = unicode(value, encoding, errors='ignore')
        except (Exception, ), exc:
            pass
        else:
            exif[key] = value
    return exif


def read_exif_gps(exif):
    gps = {}
    inf = exif.get('GPSInfo', {})
    for k in inf.keys():
        gps[GPSTAGS.get(k, k)] = inf.get(k)
    return gps


def read_exif_location(exif):
    """Extracts GPS latitide and longitude from exif data."""
    try:
        if 'GPSInfo' in exif:
            gps = exif['GPSInfo']
            latitude = (1.0 * gps[2][0][0] / gps[2][0][1]) + \
                (1.0 * gps[2][1][0] / gps[2][1][1] / 60) + \
                (1.0 * gps[2][2][0] / gps[2][2][1] / 3600)
            if gps[1] == 'S':
                latitude = -1 * latitude
            longitude = (1.0 * gps[4][0][0] / gps[4][0][1]) + \
                (1.0 * gps[4][1][0] / gps[4][1][1] / 60) + \
                (1.0 * gps[4][2][0] / gps[4][2][1] / 3600)
            if gps[3] == 'W':
                longitude = -1 * longitude
            return [latitude, longitude]
        else:
            return []
    except (Exception, ), exc:
        pass
    else:
        return []


### 


def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    #info = image._getexif()
    info = Image.open(image)._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def as_deg(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = lon = None

    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']

        gps_latitude = gps_info.get('GPSLatitude')
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = as_deg(gps_latitude)
            if gps_latitude_ref != 'N':
                lat = 0 - lat
            lon = as_deg(gps_longitude)
            if gps_longitude_ref != 'E':
                lon = 0 - lon

    return lat, lon
