from typing import Any, Callable


class Map[T]:
    def __init__(
        self,
        map_list: list[list[Any] | str],
        cast_to: type[T] = str,
        filter_function: None | Callable[[tuple[int, int], Any], bool] = None,
    ):
        self.map: dict[tuple[int, int], T] = {}

        for y, row in enumerate(map_list):
            for x, element in enumerate(row):
                if (filter_function is None) or filter_function((x, y), element):
                    self.map[x, y] = cast_to(element)  # type: ignore

    def __getitem__(self, coords: tuple[int, int]) -> T:
        return self.get(coords)

    def __setitem__(self, coords: tuple[int, int], value: T) -> None:
        self.set(coords, value)

    def __add__(self, other: "Map[T]") -> "Map[T]":
        new_map: dict[tuple[int, int], T] = self.map.copy()
        for coords, value in other.map.items():
            if coords in new_map:
                if value != new_map[coords]:
                    raise KeyError(
                        f"Both maps contain different values at coords {coords}. The values need to be the same or at least one of the maps can't contain a value for the coords."
                    )
            else:
                new_map[coords] = value

        return Map.from_dict(new_map)

    def __eq__(self, other) -> bool:
        return self.map == other.map

    def __len__(self) -> int:
        return len(self.map)

    def __str__(self) -> str:
        rows: list[str] = []

        dim_x, dim_y = self.get_dimensions()
        for y in range(dim_y):
            rows.append("")
            for x in range(dim_x):
                rows[-1] += str(self.map[x, y]) if (x, y) in self.map else " "

        return "\n".join(rows)

    @classmethod
    def from_dict(cls, dictionary: dict[tuple[int, int], T]) -> "Map[T]":
        obj = cls.__new__(cls)
        obj.map = dictionary.copy()
        return obj

    @classmethod
    def empty(cls) -> "Map[T]":
        obj = cls.__new__(cls)
        obj.map = dict()
        return obj

    def copy(self) -> "Map[T]":
        return Map.from_dict(self.map)

    def filter(self, filter: Callable[[tuple[int, int], Any], bool]) -> None:
        filtered_map: dict[tuple[int, int], T] = dict()
        for coords, value in self.map.items():
            if filter(coords, value):
                filtered_map[coords] = value

        self.map = filtered_map

    @classmethod
    def filtered(
        cls, map: "Map[T]", filter: Callable[[tuple[int, int], Any], bool]
    ) -> "Map[T]":
        filtered_map: dict[tuple[int, int], T] = dict()
        for coords, value in map.map.items():
            if filter(coords, value):
                filtered_map[coords] = value

        return Map.from_dict(filtered_map)

    def get(self, coords: tuple[int, int]) -> T:
        if coords not in self.map:
            raise KeyError(f"Coords {coords} are not in map.")

        return self.map[coords]

    def set(self, coords: tuple[int, int], value: T) -> T | None:
        old_value: T | None = self.get(coords) if coords in self.map else None
        self.map[coords] = value
        return old_value

    def get_row(self, row_number: int) -> list[tuple[tuple[int, int], T]]:
        return [
            ((x, y), value) for (x, y), value in self.map.items() if (y == row_number)
        ]

    def get_column(self, column_number: int) -> list[tuple[tuple[int, int], T]]:
        return [
            ((x, y), value)
            for (x, y), value in self.map.items()
            if (x == column_number)
        ]

    def get_all_coords(self) -> list[tuple[int, int]]:
        return [coords for coords, _ in self.map.items()]

    def get_all_values(self) -> list[T]:
        return [value for _, value in self.map.items()]

    def get_dimensions(self) -> tuple[int, int]:
        x_coords: set[int] = set()
        y_coords: set[int] = set()

        for x, y in self.map.keys():
            x_coords.add(x)
            y_coords.add(y)

        return max(x_coords) + 1, max(y_coords) + 1

    def get_inverted(self) -> dict[T, list[tuple[int, int]]]:
        inverted_map: dict[T, list[tuple[int, int]]] = dict()

        for key, value in self.map.items():
            if value not in inverted_map:
                inverted_map[value] = []

            inverted_map[value].append(key)

        return inverted_map

    def find_coords(self, search_value: T) -> tuple[int, int]:
        for coords, value in self.map.items():
            if value == search_value:
                return coords

        raise ValueError(f"Map does not contain coords with value '{search_value}'.")

    def find_coords_or_none(self, search_value: T) -> tuple[int, int] | None:
        try:
            return self.find_coords(search_value)
        except ValueError:
            return None

    def find_all_coords(self, search_value: T) -> list[tuple[int, int]]:
        found_coords: list[tuple[int, int]] = []
        for coords, value in self.map.items():
            if value == search_value:
                found_coords.append(coords)

        return found_coords

    def contains_coords(self, coords: tuple[int, int]) -> bool:
        return coords in self.map

    def check_coords_in_bounds(self, coords: tuple[int, int]) -> bool:
        if (coords[0] < 0) or (coords[1] < 0):
            return False

        dimensions = self.get_dimensions()

        if (coords[0] >= dimensions[0]) or (coords[1] >= dimensions[1]):
            return False

        return True

    def get_neighbor_coords_for_specific_directions(
        self,
        coords: tuple[int, int],
        left: bool = True,
        right: bool = True,
        up: bool = True,
        down: bool = True,
        up_left: bool = True,
        up_right: bool = True,
        down_left: bool = True,
        down_right: bool = True,
    ) -> list[tuple[int, int]]:

        if coords not in self.map:
            raise KeyError(f"Coords {coords} are not in map.")

        neighbor_coords: list[tuple[int, int]] = []

        if left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1])]
                if (coords[0] - 1, coords[1]) in self.map
                else []
            )

        if right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1])]
                if (coords[0] + 1, coords[1]) in self.map
                else []
            )

        if up:
            neighbor_coords += (
                [(coords[0], coords[1] - 1)]
                if (coords[0], coords[1] - 1) in self.map
                else []
            )

        if down:
            neighbor_coords += (
                [(coords[0], coords[1] + 1)]
                if (coords[0], coords[1] + 1) in self.map
                else []
            )

        if up_left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1] - 1)]
                if (coords[0] - 1, coords[1] - 1) in self.map
                else []
            )

        if up_right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1] - 1)]
                if (coords[0] + 1, coords[1] - 1) in self.map
                else []
            )

        if down_left:
            neighbor_coords += (
                [(coords[0] - 1, coords[1] + 1)]
                if (coords[0] - 1, coords[1] + 1) in self.map
                else []
            )

        if down_right:
            neighbor_coords += (
                [(coords[0] + 1, coords[1] + 1)]
                if (coords[0] + 1, coords[1] + 1) in self.map
                else []
            )

        return neighbor_coords

    def get_neighbors(
        self,
        coords: tuple[int, int],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> list[tuple[tuple[int, int], T]]:

        return self.get_neighbors_with_specific_directions(
            coords,
            horizontal,
            horizontal,
            vertical,
            vertical,
            diagonal,
            diagonal,
            diagonal,
            diagonal,
        )

    def get_neighbors_with_specific_directions(
        self,
        coords: tuple[int, int],
        left: bool,
        right: bool,
        up: bool,
        down: bool,
        up_left: bool,
        up_right: bool,
        down_left: bool,
        down_right: bool,
    ) -> list[tuple[tuple[int, int], T]]:

        neighbor_coords = self.get_neighbor_coords_for_specific_directions(
            coords,
            left,
            right,
            up,
            down,
            up_left,
            up_right,
            down_left,
            down_right,
        )

        return [(coords, self.map[coords]) for coords in neighbor_coords]

    def get_matching_neighbors(
        self,
        coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> list[tuple[tuple[int, int], T]]:

        neighbors = self.get_neighbors(coords, horizontal, vertical, diagonal)
        return [
            neighbor for neighbor in neighbors if matching_function(coords, neighbor)
        ]

    def has_matching_neighbors(
        self,
        coords: tuple[int, int],
        matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
        horizontal: bool = True,
        vertical: bool = True,
        diagonal: bool = True,
    ) -> bool:

        return (
            len(
                self.get_matching_neighbors(
                    coords, matching_function, horizontal, vertical, diagonal
                )
            )
            > 0
        )


def flood_fill_area[T](
    map: Map[T],
    start_coords: tuple[int, int],
    matching_function: Callable[[tuple[int, int], tuple[tuple[int, int], T]], bool],
    diagonal: bool = False,
) -> list[tuple[int, int]]:

    if not matching_function(start_coords, (start_coords, map[start_coords])):
        return []

    filled_area: list[tuple[int, int]] = []
    queue: set[tuple[int, int]] = {start_coords}

    while len(queue) > 0:
        current_coords = queue.pop()
        filled_area.append(current_coords)

        matching_neighbors = map.get_matching_neighbors(
            current_coords, matching_function, diagonal=diagonal
        )

        for coords in [
            coords for coords, _ in matching_neighbors if coords not in filled_area
        ]:
            queue.add(coords)

    return filled_area
