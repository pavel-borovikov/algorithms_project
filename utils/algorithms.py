import pandas as pd
from scipy.spatial.distance import pdist, squareform

from utils.check_solution import check_solution


def nearest_neighbour_path(data, start_position=[0,0]):
    """Find a route between all given coordinates based on the nearest neighbour of each point.
    The output will not include the start position in the output route.
    
    Best case complexity : O(n**2)


    ...

    Attributes :
    ------------
    data : pandas DataFrame
                    x and y coordinates, with unique indices

    end_position : list
                    x and y coordinates of the final destination
                    defaults to [0,0]

    -------

    Ouput :

    A list of indices of the nearest neighbour route between the coordinates.
    This list starts at the start_position coordinates, which default to [0,0].

    """

    # Adding the start position to the DataFrame
    end_index = data.index.max()+1 # making sure it's a new index being used
    start_point = pd.DataFrame(data=[start_position], columns=data.columns, index=[end_index])

    # The new DataFrame will have new indices
    # a new column will appear with the old indices
    data = pd.concat([data, start_point]).reset_index()

    # distances is a 2D array that will contain euclidean distances between each points
    distances = squareform(pdist(data.drop(columns=['index'])))


    # the search will begin here and update the index after each point
    search_index = data.iloc[-1].name

    # a list of new indices used by the search algorithm
    visited = [search_index]

    while len(visited) != len(distances):

        shortest_distance = float('inf')
        index_shortest_distance = float('inf')

        for i in range(len(distances[search_index])):

            # the same point will have a distance of 0
            # it must be avoided
            if i == search_index:
                    continue
            
            if i not in visited:
                if distances[search_index, i] < shortest_distance:

                    shortest_distance = distances[search_index, i]
                    index_shortest_distance = i


        # preparing the next point for the search
        visited.append(index_shortest_distance)
        search_index = index_shortest_distance


    # once the search is complete,
    # create a route with the original indices
    route = list(map(lambda x: data['index'].iloc[x], visited[1:]))

    return route[::1]