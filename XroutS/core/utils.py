# from XroutS.core.models import AppUser
import random


# def get_user_by_slug(user_slug):
#     # TODO fix username when autherazation
#     return AppUser.objects.get(slug=user_slug)

def generate_random_number():
    return random.randint(1000, 9999)

import math

def haversine(coord1, coord2):
    R = 6371  # Earth radius in kilometers

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance