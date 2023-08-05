import numpy as np

import super_utils as sutils

def intersect(poly):
    poly = sutils.parse_geojson(poly)

    for p in poly:
        print p