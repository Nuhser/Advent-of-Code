import heapq as heap

from collections import defaultdict

def dijkstra(map: dict[tuple[int, int], list[tuple[tuple[int, int], int]]], starting_point: tuple[int, int], end_point: (None | tuple[int, int])=None) -> tuple[dict[tuple[int, int], tuple[int,int]], defaultdict[tuple[int, int], (int | float)]]:
    """
    This method calculates the lowest cost to get to every point on a map starting at starting_point as well as every points parent on the cheapest path from the starting point to that point.

    Parameter
    ---------
    map : dict[tuple[int, int], list[tuple[tuple[int, int], int]]]
        A map of points where the key is a tuple of the points x- and y-coordinates and the value is a list of every adjacent point and the cost/weight to get to this point.

    starting_point : tuple[int, int]
        The x- and y-coordinates of the starting point of the cost calculations.

    Returns
    -------
    parent_map, costs
        Two dictionaries which both use the x- and y-coordinates of the points on the map as theier keys. parent_map has the parent of the individual point on the cheapest path beginning at the starting point as its value and costs the cost to get to this point.
    """

    visited = set()
    parents_map: dict[tuple[int, int], tuple[int,int]] = {}
    costs: defaultdict[tuple[int, int], (int | float)] = defaultdict(lambda: float("inf"))
    costs[starting_point] = 0
    priority_queue = []
    heap.heappush(priority_queue, (0, starting_point))

    while priority_queue:
        _, point = heap.heappop(priority_queue)
        visited.add(point)

        for adjacent_point, weight in map[point]:
            if adjacent_point in visited:
                continue

            new_cost = costs[point] + weight
            if new_cost < costs[adjacent_point]:
                parents_map[adjacent_point] = point
                costs[adjacent_point] = new_cost
                heap.heappush(priority_queue, (new_cost, adjacent_point))

        if (end_point != None) and (end_point == point):
            break

    return parents_map, costs