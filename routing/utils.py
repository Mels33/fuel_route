import csv
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(float, [lon1, lat1, lon2, lat2])
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    miles = 3956 * c
    return miles

def get_stations():
    stations = []
    with open('routing/fuel_data_with_coords.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            if row['lat'] and row['lon']:
                stations.append({
                    'id': f"station_{idx}",
                    'name': row['Truckstop Name'],
                    'address': row['Address'],
                    'city': row['City'],
                    'state': row['State'],
                    'price': float(row['Retail Price']),
                    'lat': float(row['lat']),
                    'lon': float(row['lon']),
                })
    return stations