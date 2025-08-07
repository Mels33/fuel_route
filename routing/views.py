from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_stations
from .graph_route import build_graph_k_nearest, add_start_finish, find_best_path
import requests


def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "countrycodes": "us", "format": "json", "limit": 1}
    headers = {'User-Agent': 'TruckstopGeocoder/1.0'}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None


class OptimalRouteView(APIView):
    def post(self, request):
        start = request.data['start']
        finish = request.data['finish']
        start_coord = geocode(start)
        finish_coord = geocode(finish)

        if not start_coord or not finish_coord:
            return Response({'error': 'Could not geocode addresses'}, status=400)

        stations = get_stations()
        G = build_graph_k_nearest(stations)
        start_id, finish_id = add_start_finish(G, stations, start_coord, finish_coord)
        path = find_best_path(G, start_id, finish_id)

        if not path:
            return Response({'error': 'No route found'}, status=404)

        stops = []
        total_cost = 0
        prev = path[0]

        for p in path[1:-1]:
            node = G.nodes[p]
            stops.append({
                'name': node['name'],
                'address': node['address'],
                'city': node['city'],
                'state': node['state'],
                'lat': node['lat'],
                'lon': node['lon'],
                'price': node['price'],
            })
            edge = G.edges[prev, p]
            total_cost += edge['weight']
            prev = p

        edge = G.edges[prev, path[-1]]
        total_cost += edge['weight']

        coordinates = []
        for node_id in path:
            node_data = G.nodes[node_id]
            coordinates.append({
                'lat': node_data['lat'],
                'lon': node_data['lon']
            })

        route_url = (
                "https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=" +
                ';'.join(f"{coord['lat']},{coord['lon']}" for coord in coordinates)
        )

        return Response({
            'total_fuel_cost': round(total_cost, 2),
            'route_url': route_url
        })
