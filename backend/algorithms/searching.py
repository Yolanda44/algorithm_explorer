from typing import Any, Dict, List


def linear_search(numbers: List[float], target: float) -> Dict[str, Any]:
    steps: List[Dict[str, int]] = []
    for idx, value in enumerate(numbers):
        steps.append({"checked": idx})
        if value == target:
            return {"index": idx, "steps": steps}
    return {"index": -1, "steps": steps}


def binary_search(numbers: List[float], target: float) -> Dict[str, Any]:
    steps: List[Dict[str, int]] = []
    low, high = 0, len(numbers) - 1

    while low <= high:
        mid = (low + high) // 2
        steps.append({"checked": mid})
        if numbers[mid] == target:
            return {"index": mid, "steps": steps}
        if numbers[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return {"index": -1, "steps": steps}


def recursive_binary_search(numbers: List[float], target: float) -> Dict[str, Any]:
    steps: List[Dict[str, int]] = []

    def _search(low: int, high: int) -> int:
        if low > high:
            return -1
        mid = (low + high) // 2
        steps.append({"checked": mid})
        if numbers[mid] == target:
            return mid
        if numbers[mid] < target:
            return _search(mid + 1, high)
        return _search(low, mid - 1)

    index = _search(0, len(numbers) - 1)
    return {"index": index, "steps": steps}
