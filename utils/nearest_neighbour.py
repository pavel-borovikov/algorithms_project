
import pandas as pd
from scipy.spatial.distance import pdist, squareform

def nearest_neighbour(banks, end_position=(0,0)):
    """Find a route between all given banks based on the closest neighbour of each point.
    
    Complexity (at best) : O(n**2)

    ...

    Attributes :
    ------------
    banks : pandas.DataFrame object
            must contain specified columns 'id', 'x_coordinate', 'y_coordinate'

    end_position : tuple of coordinates on the graph
            defaults to (0,0)

    -------

    Ouput :

    A list of bank ids to travel to.

    """

    # names of columns stored here in case
    # of future modification
    id = 'id'
    x = 'x_coordinate'
    y = 'y_coordinate'


    # filtering out and keeping only useful information
    banks = banks[[id, x, y]]

    # Creating a new location for the final destination
    final_id = banks[id].max() + 1
    final_location = pd.Series({id : final_id, x : end_position[0], y : end_position[1]})

    banks = pd.concat([banks, final_location])

    distances = squareform(pdist(banks[[x, y]]))



    route = []

    # The 'end position' index in the distances array
    start_idx = -1
    # The search will start searching from here

    visited = [start_idx]
    while len(visited) != len(distances):

        smallest = float('inf')
        # store the index of the point with the shortest distance
        idx = 0

        # For every distance between given points, find the smallest
        for i in range(len(distances[start_idx])):
            if i not in visited:
                if distances[start_idx,i] == 0.0:
                    continue

                if distances[start_idx,i] < smallest:
                    smallest = distances[start_idx,i]
                    idx = i

        # Starting a new search for the next index
        visited.append(idx)
        start_idx = idx

    # When the search is complete 
    for i in visited:
        if banks.iloc[i]['id'] == 10001:
            continue
        else:
            route.append(banks.iloc[i]['id'])

    return route[::-1]