import pandas as pd
from scipy.spatial.distance import pdist, squareform

from utils.check_solution import check_solution


def nearest_neighbour_path(data, end_position=[0,0], return_path_length=False):
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
    This list starts at the end_position coordinates, which default to [0,0].

    """

    # Adding the start position to the DataFrame
    end_index = data.index.max()+1 # making sure it's a new index being used
    start_point = pd.DataFrame(data=[end_position], columns=data.columns, index=[end_index])

    # The new DataFrame will have new indices
    # a new column will appear with the old indices
    data = pd.concat([data, start_point]).reset_index()

    # distances is a 2D array that will contain euclidean distances between each points
    distances = squareform(pdist(data.drop(columns=['index'])))
    
    path_length = 0


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


        # adding distance to total path length
        path_length += shortest_distance


        # preparing the next point for the search
        visited.append(index_shortest_distance)
        search_index = index_shortest_distance


    # once the search is complete,
    # create a route with the original indices
    route = list(map(lambda x: data['index'].iloc[x], visited[1:]))


    if return_path_length == True:
        return path_length

    else:
        return route[::1]


def inc_nearest_neighbour_path(df, start=0, increments=0.01):

    # storing variables for useful data
    best_money = float('-inf')
    best_time_remaining = float('inf')
    best_route = []

    while best_time_remaining > 0:
        mask = df.loc[(df['score'] > start)]
        test_df = mask[['x_coordinate','y_coordinate']]

        # using a nearest neighbour algorithm
        # with start position at 0,0 then reversed 
        # the 0,0 will be the end point of this project
        solution = nearest_neighbour_path(test_df, end_position=[0,0])

        # the check solution function looks at the euclidean distances
        # between each given bank id
        try:
            # if the 24h limit is exceeded, the check_solution function throws an error
            total_money, time_remaining = check_solution(solution, df)

            if total_money > best_money:
                best_money = total_money
                best_time_remaining = time_remaining
                best_route = solution

            start += increments

        except:
            break


    total_distance = round(nearest_neighbour_path(test_df[['x_coordinate', 'y_coordinate']], return_path_length=True), 2)

    info = {'money_earned' : best_money,
            'time_remaining' : f'{round(best_time_remaining, 2)} hours',
            'banks_visited' : len(best_route),
            'lowest_bank_score' : round(start-increments, 3),
            'total_path_length' : total_distance,
            'best_route' : best_route
            }

    return info