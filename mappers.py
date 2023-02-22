from itertools import combinations
#import folium
import math
import osmnx as ox
import folium
ox.config(log_console=True, use_cache=True)
import networkx as nx

import algorithms as a
import models
import matrices
import annealing


def map_ms_tree(area_min, area_max, coord_list, max_dist, algo_select):
    
    graph = ox.graph.graph_from_bbox(north=area_min[0], south=area_max[0], east=area_min[1], 
                                     west=area_max[1], network_type = "drive")

    node_list = []
    for coord in coord_list:
        node_list.append(ox.distance.nearest_nodes(graph, coord[1], coord[0]))

    distances = {}
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            try:
                distance = nx.shortest_path_length(graph, node_list[i], node_list[j], 
                                                   weight="length", method='dijkstra')
            except nx.exception.NetworkXNoPath:
                distance = math.inf

            if distance <= max_dist:
                distances[(i,j)] = distance

    nodes = range(len(node_list))

    if algo_select == "1":
        tree = a.kruskal(nodes, distances)
    elif algo_select == "2":
        print(matrices.minimum_spanning_tree(nodes, distances, 10000)) 
        exit()
   
    route_map = None
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            if (i,j) in tree:
                route = nx.shortest_path(graph, node_list[i], node_list[j], 
                                         weight="length", method='dijkstra')             
                route_map = ox.plot_route_folium(graph, route, route_map=route_map, 
                                                 color=["#1133FF"], opacity=0.5)
   
    for coord in coord_list:
            folium.CircleMarker(coord, radius = 5,color="blue",fill=True, fill_color="blue", 
                                fill_opacity=0.9).add_to(route_map)


    route_map.save("tree.html")
    

def map_steiner_tree(area_min, area_max, coord_list, n_coord_list, max_dist, algo_select):

    full_coord_list = coord_list + n_coord_list

    graph = ox.graph.graph_from_bbox(north=area_min[0], south=area_max[0], east=area_min[1],
                                     west=area_max[1], network_type = "drive")

    node_list = []
    for coord in full_coord_list:
        node_list.append(ox.distance.nearest_nodes(graph, coord[1], coord[0]))

    distances = {}
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            try:
                distance = nx.shortest_path_length(graph, node_list[i], node_list[j], 
                                                   weight="length", method='dijkstra')
            except nx.exception.NetworkXNoPath:
                distance = math.inf

            if distance <= max_dist:
                distances[(i,j)] = distance

    nodes = list(range(len(coord_list)))
    n_nodes = list(range(len(coord_list), len(full_coord_list)))

    if algo_select == "1":
        tree = a.steiner_heuristic(nodes, n_nodes, distances)
    else:
        pass    
   
    route_map = None
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            if (i,j) in tree:
                route = nx.shortest_path(graph, node_list[i], node_list[j], 
                                         weight="length", method='dijkstra')             
                route_map = ox.plot_route_folium(graph, route, route_map=route_map, 
                                                 color=["#1133FF"], opacity=0.5)
  
    for i in nodes:
            folium.CircleMarker(full_coord_list[i], radius = 5,color="blue",fill=True, 
                                fill_color="blue", popup = str(i), 
                                fill_opacity=0.9).add_to(route_map)
     
    for i in n_nodes:
            folium.CircleMarker(full_coord_list[i], radius = 5,color="#999999",fill=True, 
                                fill_color="#999999", popup = str(i), 
                                fill_opacity=0.9).add_to(route_map)



    route_map.save("steiner_tree.html")


def map_vertex_cover(area_min, area_max, coord_list, max_dist, algo_select):
       
    graph = ox.graph.graph_from_bbox(north=area_min[0], south=area_max[0], east=area_min[1], 
                                     west=area_max[1], network_type = "drive")

    node_list = []
    for coord in coord_list:
        node_list.append(ox.distance.nearest_nodes(graph, coord[1], coord[0]))

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

    if algo_select == "1":
        selected_nodes = a.cover_heuristic(nodes, edges)
    elif algo_select == "2":
        print(matrices.vertex_cover(nodes, edge, 100)) 
        exit()
   
    route_map = None
    for edge in edges:
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

    route_map.save("cover.html")


def map_set_cover(area_min, area_max, coord_list, max_dist, algo_select):     
    
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

    if algo_select == "1":
        selected_nodes = a.cover_heuristic_2(nodes, edges)
    elif algo_select == "2":
        model = models.set_cover(nodes, edges, 10)
        annealing.anneal(model) 
        exit()
   
    route_map = None
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
            
    route_map.save("cover2.html")

    print(nodes)
    print(edges)
    print(selected_nodes)

