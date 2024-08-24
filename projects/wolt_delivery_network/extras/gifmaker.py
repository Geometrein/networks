import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import networkx as nx
import osmnx as ox
import imageio as iio
import matplotlib
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')



def get_shortest_paths(G: nx.Graph, origin_nodes: list, destination_nodes: list, weight: str) -> tuple:
    """
    This function calculates the shortest paths based on weight parameter.
    ---
    Args:
        G (nx.Graph): input Graph
        origin_nodes (list): list of origin nodes
        destination_nodes (list): list of destination nodes
        weight (str): graph property for shortest path calculation
    Returns: None
    """
    route_list = []
    nan_index_list = []

    for index, node in enumerate(origin_nodes):
        origin = origin_nodes[index]
        destination = destination_nodes[index]
        route = ox.shortest_path(G, origin, destination, weight=weight)

        if route and isinstance(route, list):
            route_list.append(route)
        else:
            nan_index_list.append(index)

    print(f'''Generated {len(route_list)} routes from {len(origin_nodes)}
        origins and {len(destination_nodes)}destinations.''')
    print(f'{len(nan_index_list)} routes returned NaN.')

    return route_list, nan_index_list


def get_shortest_path_lengths(G: nx.Graph, origin_nodes: list, destination_nodes: list, weight: str):
    """
    This function calculates the shortest paths based on weight parameter.
    ---
    Args:
        origin_nodes (list): list of origin nodes
        destination_nodes (list): list of destination nodes
        weight (str): graph property for shortest path calculation
    """
    length_list = []
    nan_index_list = []

    for index, node in enumerate(origin_nodes):
        origin = origin_nodes[index]
        destination = destination_nodes[index]
        try:
            length = nx.shortest_path_length(G, source=origin, target=destination, weight=weight)
            length_list.append(length)
        except:
            nan_index_list.append(index)
    
    print(f'''Generated {len(length_list)} routes from {len(origin_nodes)}
        origins and {len(destination_nodes)}destinations.''')
    print(f'{len(nan_index_list)} routes returned NaN.')
    
    return length_list, nan_index_list


def make_mapper(lst: list) -> tuple:
    """
    This function makes Matplotlib scalarMapper for the route colors.
    ---
    Args:
        lst (list): list containing route lengths
    Returns:
        tuple (tuple): (Matplotlib scalarMapper (list) and color_list (list))
    """
    cmap = plt.cm.get_cmap('plasma_r')
    minima = min(lst)
    maxima = max(lst)

    norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=cmap)

    color_list = []

    for v in lst:
        color_list.append(mapper.to_rgba(v))

    return mapper, color_list


def create_g(df: pd.DataFrame) -> tuple:
    """
    This function creates a base graph to plot on.
    ---
    Args:
        df (pd.DataFrame): 
    Returns:
        tuple (tuple): (nx.Graph object, origin nodes (list) dest. nodes (list))
    """
    centroid = [60.1699, 24.9384]
    mode = "drive"
    G = ox.graph_from_point(centroid, dist=4000, simplify=True, network_type=mode)

    origin_nodes = ox.distance.nearest_nodes(G, X=df['VENUE_LONG'], Y=df['VENUE_LAT'])
    destination_nodes = ox.distance.nearest_nodes(G, X=df['USER_LONG'], Y=df['USER_LAT'])

    return G, origin_nodes, destination_nodes


def plot_routes(G: nx.Graph, df: pd.DataFrame, start, end, hour, day, mapper):
    """
    This function Plots routes within a specified date range.
    ---
    Args:
        G (nx.Graph): Input graph
        df (pd.DataFrame): input dataframe
        start (datetime): index for filtering the routes
        end (datetime): index for filtering the routes
        hour (int): integer hour 0-24
        day (int): integer date 1-31
        mapper: Matplotlib scalarMapper

    Returns: None
    """

    filtered_df = df[(df['TIMESTAMP'] >= start) & (df['TIMESTAMP'] <= end)]
    routes_to_plot = filtered_df['routes'].tolist()
    route_colors = filtered_df['route_color'].tolist()
    fig, ax = ox.plot_graph_routes(G,
                                   routes=routes_to_plot,
                                   figsize=(32, 18),
                                   route_colors=route_colors,
                                   route_linewidth=5,
                                   route_alpha=.9,
                                   save=False,
                                   show=False,
                                   edge_color='grey',
                                   node_color='grey',
                                   bgcolor='white',
                                   node_size=7)

    filepath = f'images/day_{day}_hour_{hour}.jpg'
    cb = fig.colorbar(mapper,
                      ax=ax,
                      orientation='vertical',
                      fraction=0.05,
                      pad=0.1)
    
    cb.set_label('Courier Travel Distance (km)', fontsize=40)
    cb.ax.tick_params(labelsize=25)
    fig.suptitle(f'Helsinki Food Deliveries {day}.08.2020  {hour}:00', fontsize=50)
    fig.set_dpi(300)
    fig.savefig(filepath, facecolor='white', transparent=False)


def generate_images(G: nx.Graph, df: pd.DataFrame, mapper: list) -> None:
    """
    This function generates each frame of the animation.
    ---
    Args:
        G (nx.Graph):
        df (pd.DataFrame):
        mapper (list):

    Returns: None
    """
    year = 2020
    month = 8
    day_range = range(1, 15)
    hour_range = range(7, 20)

    for day in day_range:
        for hour in hour_range:
            next_hour = hour + 1
            start = datetime(year, month, day, hour)
            end = datetime(year, month, day, next_hour)

            plot_routes(G, df, start, end, hour, day, mapper)


def generate_video(path: str) -> None:
    """
    This function generates the video.
    ---
    Args:
        path (str): Path to image frames.
    Returns: None
    """
    images = list()
    for file in sorted(Path(path).iterdir()):
        im = iio.imread(file)
        images.append(im)

    writer = iio.get_writer('test.mp4', fps=4)

    for img in images:
        writer.append_data(img)


def gifmaker(path: str) -> None:
    """
    This function generates the video.
    ---
    Args:
        path (str): Path to image frames.
    Returns: None
    """
    images = list()
    for file in sorted(Path(path).iterdir()):
        im = iio.imread(file)
        images.append(im)

    duration = 0.35
    iio.mimsave(f'wolt_{duration}.gif', images, duration=duration)


def main(generate_gif: bool, generate_mp4: bool):
    """
    I am singing in the main().
    """
    path = 'images/'
    filenames = os.listdir(path)

    if len(filenames) == 0:
        df = pd.read_csv('data/orders_autumn_2020.csv')
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        #print(df.head())

        G, origin_nodes, destination_nodes = create_g(df)

        weight = 'travel_time'
        route_list, nan_index = get_shortest_paths(G, origin_nodes, destination_nodes, weight)

        weight = 'length'
        length_list, nan_index = get_shortest_path_lengths(G, origin_nodes, destination_nodes, weight)
        length_list = [i/1000 for i in length_list]
        mapper, color_list = make_mapper(length_list)

        df = df.drop(df.index[nan_index])
        df['routes'] = route_list
        df['route_length'] = length_list
        df['route_color'] = color_list

        print(len(nan_index))

        generate_images(G, df, mapper)

    if generate_gif:
        gifmaker(path)

    if generate_mp4:
        generate_video(path)

    print('done')


if __name__ == '__main__':
    main(generate_gif=False, generate_video=False)
