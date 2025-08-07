import networkx as nx
import numpy as np
from sklearn.neighbors import BallTree
from .utils import haversine, get_stations

MAX_RANGE_MILES = 500
K_NEIGHBORS = 1000


def build_graph_k_nearest(stations, k=K_NEIGHBORS, max_dist=MAX_RANGE_MILES):
    G = nx.DiGraph()
    coords = np.array([[s['lat'], s['lon']] for s in stations])
    tree = BallTree(np.radians(coords), metric='haversine')
    for idx, s in enumerate(stations):
        G.add_node(s['id'], **s)
        dist, ind = tree.query([np.radians([s['lat'], s['lon']])], k=k + 1)
        for d, j in zip(dist[0], ind[0]):
            if j == idx:
                continue
            miles = d * 3956
            if 0 < miles <= max_dist:
                gallons_needed = miles / 10
                fuel_cost = gallons_needed * s['price']
                G.add_edge(s['id'], stations[j]['id'], weight=fuel_cost, distance=miles)
    return G


def add_start_finish(G, stations, start_coord, finish_coord, max_dist=MAX_RANGE_MILES):
    start_id = 'start'
    finish_id = 'finish'
    G.add_node(start_id, lat=start_coord[0], lon=start_coord[1])
    G.add_node(finish_id, lat=finish_coord[0], lon=finish_coord[1])
    coords = np.array([[s['lat'], s['lon']] for s in stations])
    tree = BallTree(np.radians(coords), metric='haversine')
    dist, ind = tree.query([np.radians([start_coord[0], start_coord[1]])], k=K_NEIGHBORS)
    for d, j in zip(dist[0], ind[0]):
        miles = d * 3956
        if miles <= max_dist:
            gallons_needed = miles / 10
            fuel_cost = gallons_needed * stations[j]['price']
            G.add_edge(start_id, stations[j]['id'], weight=fuel_cost, distance=miles)
    dist, ind = tree.query([np.radians([finish_coord[0], finish_coord[1]])], k=K_NEIGHBORS)
    for d, j in zip(dist[0], ind[0]):
        miles = d * 3956
        if miles <= max_dist:
            gallons_needed = miles / 10
            fuel_cost = gallons_needed * stations[j]['price']
            G.add_edge(stations[j]['id'], finish_id, weight=fuel_cost, distance=miles)
    return start_id, finish_id


def find_best_path(G, start_id, finish_id):
    try:
        path = nx.shortest_path(G, source=start_id, target=finish_id, weight='weight')
    except nx.NetworkXNoPath:
        return None
    return path
