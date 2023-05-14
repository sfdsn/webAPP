from PIL import Image
from PIL.ExifTags import TAGS
import os
import math

def sort_photos_by_date(imgPilObjs):

    photos_obj = []
    for imgPilObj in imgPilObjs:

        date_taken = imgPilObj[1]._getexif()[36867] 
        new = (date_taken,imgPilObj)

        photos_obj.append(new)
    photos_obj.sort()
    return [photo[1] for photo in photos_obj]
def get_exif_data(pilImgObj):

    exif_data = {}
    img = pilImgObj
    if hasattr(img, '_getexif'):
        exif_info = img._getexif()
        if exif_info is not None:
            for tag, value in exif_info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    return exif_data

def get_gps_info(image):

    exif_data = get_exif_data(image)
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode_key = TAGS.get(key, key)
            gps_info[decode_key] = exif_data['GPSInfo'][key]
    return gps_info

def convert_to_degrees(value):

    d, m, s = value[0], value[1], value[2]
    return d + (m / 60.0) + (s / 3600.0)

def get_coordinates(info):



    lat = convert_to_degrees(info[2])

    lat_ref = info['InteropIndex']
    if lat_ref == 'S':
        lat *= -1
    lon = convert_to_degrees(info[4])
    lon_ref = info[3]
    if lon_ref == 'W':
        lon *= -1

    alt = info[6]
    return lat, lon,alt


def get_all_coordinates(pilImgObjs):

    coordinates = []
    for pilImgObj in pilImgObjs:
        gps_info = get_gps_info(pilImgObj[1])
        if gps_info:
            lat,lon,alt = get_coordinates(gps_info)
            imgName = pilImgObj[0]
            coordinates.append([imgName,lat,lon,alt])
    return coordinates 



def distance(coor1, coor2):

    lat1 = coor1[1]
    lon1 = coor1[2]
    lat2 = coor2[1]
    lon2 = coor2[2]
    R = 6371  
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) ** 2 + \
        math.sin(dLon / 2) ** 2 * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    distance = d * 1000
    return '%.3f'%distance


