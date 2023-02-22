from itertools import combinations
#import folium
import math
import osmnx as ox
import folium
ox.config(log_console=True, use_cache=True)
import networkx as nx
import time
import random

import algorithms as a
import models
import annealing

def graph_set_cover(nodes, edge_prob, algo_select, prob_select, weight):
    node_list = []
    edge_list = []
    for j in range(nodes):
        node_list.append(j)
        
        for k in range(0,j):
            if random.uniform(0,1) < edge_prob:
                edge_list.append((k,j))


    start_time = time.time()

    if algo_select == "1":
        if prob_select == "1":
            selected_nodes = a.cover_heuristic_2(node_list, edge_list)
        elif algo_select =="2":
            selected_nodes = a.cover_heuristic(node_list, edge_list)
    elif algo_select == "2":
        if prob_select == "1":
            model = models.set_cover(node_list, edge_list, weight)
        elif algo_select =="2":
            model = models.vertex_cover(node_list, edge_list, weight)
        selected_nodes = annealing.anneal(model)

    runtime = time.time() - start_time

    print(edge_list)
    print(selected_nodes)

    return(len(selected_nodes), runtime)


def map_set_cover(area_min, area_max, coord_list, max_dist, algo_select, prob_select, is_last, weight):     
    
    graph = ox.graph.graph_from_bbox(north=area_min[0], south=area_max[0], east=area_min[1],
                                     west=area_max[1], network_type = "drive")

    node_list = []
    for coord in coord_list:
        node_list.append(ox.distance.nearest_nodes(graph, coord[1], coord[0]))

    route = {}
    edges = []
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            try:
                distance = nx.shortest_path_length(graph, node_list[i], node_list[j], 
                                                   weight="length", method='dijkstra')             
            except nx.exception.NetworkXNoPath:
                distance = math.inf
            if distance <= max_dist:
                    edges.append((i,j))

    nodes = list(range(len(node_list)))

    print("edges" + str(edges))

    start_time = time.time()

    if algo_select == "1":
        if prob_select == "1":
            selected_nodes = a.cover_heuristic_2(nodes, edges)
        elif prob_select =="2":
            selected_nodes = a.cover_heuristic(nodes, edges)
    elif algo_select == "2":
        if prob_select == "1":
            model = models.set_cover(nodes, edges, weight)
        elif prob_select =="2":
            model = models.vertex_cover(nodes, edges, weight)
        print(model)
        selected_nodes = annealing.anneal(model)

    runtime = time.time() - start_time

    print(nodes)
    print(edges)
    print(selected_nodes)

    
    if (is_last):
        try:
            route_map = None
            #dummy_route = nx.shortest_path(graph, node_list[0], node_list[1], 
            #                                     weight="length", method='dijkstra')   
            #route_map = ox.plot_route_folium(graph, dummy_route, route_map=route_map, color=["#1133FF"], opacity=0)
            for node in selected_nodes:
                for edge in edges:
                    if edge[0] == node or edge[1] == node:
                        route = nx.shortest_path(graph, node_list[edge[0]], node_list[edge[1]], 
                                                weight="length", method='dijkstra')   
                        route_map = ox.plot_route_folium(graph, route, route_map=route_map, 
                                                        color=["#1133FF"], opacity=0.5)

            for i in nodes:
                if i in selected_nodes:
                    folium.CircleMarker(coord_list[i], radius = 5,color="blue",fill=True, 
                                        fill_color="blue", fill_opacity=0.9).add_to(route_map)
                else:
                    folium.CircleMarker(coord_list[i], radius = 5,color="#999999",fill=True, 
                                        fill_color="#999999", fill_opacity=0.9).add_to(route_map)
                    
            route_map.save("covert" + str(len(nodes)) + ".html")
        except:
            print("Map error")

    return(len(selected_nodes), runtime)

