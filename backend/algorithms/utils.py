from typing import Callable, Dict, List

from . import searching, sorting

Sorter = Callable[[List[float]], Dict[str, object]]
Searcher = Callable[[List[float], float], Dict[str, object]]


def normalize_algorithm(name: str) -> str:
    return name.strip().lower()


SORTING_ALGORITHMS: Dict[str, Sorter] = {
    "bubble": sorting.bubble_sort,
    "bubble sort": sorting.bubble_sort,
    "insertion": sorting.insertion_sort,
    "insertion sort": sorting.insertion_sort,
    "merge": sorting.merge_sort,
    "merge sort": sorting.merge_sort,
    "quick": sorting.quick_sort,
    "quick sort": sorting.quick_sort,
}

SEARCHING_ALGORITHMS: Dict[str, Searcher] = {
    "linear": searching.linear_search,
    "linear search": searching.linear_search,
    "binary": searching.binary_search,
    "binary search": searching.binary_search,
    "recursive binary": searching.recursive_binary_search,
    "recursive binary search": searching.recursive_binary_search,
    "recursive-binary": searching.recursive_binary_search,
}
