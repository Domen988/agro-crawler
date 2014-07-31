import GaussKruegerToWGS

right = 396678
height = 91724
right += 5000000
height += 5000000

r1, y1, = GaussKruegerToWGS.convert_GK_to_lat_long(right, height, use_wgs84=None)
print r1, y1