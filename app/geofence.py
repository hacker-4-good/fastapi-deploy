import math

LAT = 28.545787
LON = 77.190832
RADIUS = 200

def distance(lat1, lon1):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(LAT)
    dphi = math.radians(LAT - lat1)
    dlambda = math.radians(LON - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))


def is_inside(lat, lon):
    print(distance(lat, lon))
    return distance(lat, lon) <= RADIUS