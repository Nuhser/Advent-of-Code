from __future__ import annotations
from dataclasses import dataclass
from .sorting import heap_sort


class KDTree:
    def __init__(self, nodes: list[tuple[int, ...]]):
        if len(nodes) < 1:
            raise ValueError('"nodes" need to have at least one element.')

        self.dimensions: int = len(nodes[0])
        self.nodes: TreeNode | None = build_tree_recursively(nodes, self.dimensions)


@dataclass
class TreeNode:
    value: tuple[int, ...]
    left: TreeNode | None
    right: TreeNode | None


def build_tree_recursively(
    nodes: list[tuple[int, ...]], dimensions: int, current_dimension: int = 0
) -> TreeNode | None:

    if len(nodes) < 1:
        return None

    middle_idx: int = len(nodes) // 2

    if len(nodes) == 1:
        return TreeNode(nodes[middle_idx], None, None)

    # sort nodes by relevant dimension
    heap_sort(
        nodes, lambda node1, node2: node2[current_dimension] > node1[current_dimension]
    )

    left_nodes: list[tuple[int, ...]] = nodes[:middle_idx]
    right_nodes: list[tuple[int, ...]] = nodes[middle_idx + 1 :]

    return TreeNode(
        nodes[middle_idx],
        build_tree_recursively(
            left_nodes, dimensions, (current_dimension + 1) % dimensions
        ),
        build_tree_recursively(
            right_nodes, dimensions, (current_dimension + 1) % dimensions
        ),
    )
