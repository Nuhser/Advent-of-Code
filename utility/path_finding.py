import heapq as heap

from collections import defaultdict

def dijkstra(
        map: dict[tuple[int, int], list[tuple[tuple[int, int], int]]],
        starting_point: tuple[int, int],
        end_point: (None | tuple[int, int]) = None,
        max_length_same_direction: (int | float) = float("inf")
) -> tuple[dict[tuple[int, int], tuple[int,int]], defaultdict[tuple[int, int], (int | float)]]:
    """
    This method calculates the lowest cost to get to every point on a map starting at starting_point as well as every points parent on the cheapest path from the starting point to that point.

    Parameter
    ---------
    map : dict[tuple[int, int], list[tuple[tuple[int, int], int]]]
        A map of points where the key is a tuple of the points x- and y-coordinates and the value is a list of every adjacent point and the cost/weight to get to this point.

    starting_point : tuple[int, int]
        The x- and y-coordinates of the starting point of the cost calculations.

    end_point : (None | tuple[int, int]) = None
        The x- and y-coordinates of the end point of the cost calculations. If set to None, the calculation won't stop until the costs to get to all points in the map are calculated.

    Returns
    -------
    parent_map, costs
        Two dictionaries which both use the x- and y-coordinates of the points on the map as theier keys. parent_map has the parent of the individual point on the cheapest path beginning at the starting point as its value and costs the cost to get to this point.
    """

    visited: set[tuple[tuple[int, int], tuple[int, int], int]] = set()
    parents_map: dict[tuple[int, int], tuple[int,int]] = {}

    direction_map: dict[tuple[int, int], tuple[tuple[int, int], int]] = {(0, 0): ((0, 0), 0)}

    costs: defaultdict[tuple[int, int], (int | float)] = defaultdict(lambda: float("inf"))
    costs[starting_point] = 0

    priority_queue: list = []
    heap.heappush(priority_queue, (0, starting_point, (0, 0), 0))

    while priority_queue:
        _, point, point_direction, point_moved_blocks = heap.heappop(priority_queue)

        if (point, point_direction, point_moved_blocks) in visited:
            continue

        visited.add((point, point_direction, point_moved_blocks))

        for adjacent_point, weight in map[point]:
            direction = (adjacent_point[0] - point[0], adjacent_point[1] - point[1])

            if (direction == direction_map[point][0]):
                moved_blocks = direction_map[point][1] + 1

                if (moved_blocks > max_length_same_direction):
                    continue

            else:
                moved_blocks = 1

            new_cost = costs[point] + weight
            if new_cost >= costs[adjacent_point]:
                continue

            parents_map[adjacent_point] = point
            direction_map[adjacent_point] = (direction, moved_blocks)
            costs[adjacent_point] = new_cost
            heap.heappush(priority_queue, (new_cost, adjacent_point, direction, moved_blocks))

        if (end_point != None) and (end_point == point):
            break

    return parents_map, costs


def is_in_manhattan_distance(point1: tuple[int, int], point2: tuple[int, int], max_manhattan_distance: int) -> bool:
    return max_manhattan_distance >= get_manhatten_distance(point1, point2)


def get_manhatten_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])