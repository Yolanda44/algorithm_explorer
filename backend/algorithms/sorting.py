from typing import Any, Dict, List


def bubble_sort(numbers: List[float]) -> Dict[str, Any]:
    arr = list(numbers)
    steps: List[List[float]] = []
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr.copy())

    return {"sorted": arr, "steps": steps}


def insertion_sort(numbers: List[float]) -> Dict[str, Any]:
    arr = list(numbers)
    steps: List[List[float]] = []

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append(arr.copy())
            j -= 1
        arr[j + 1] = key
        if j + 1 != i:
            steps.append(arr.copy())

    return {"sorted": arr, "steps": steps}


def merge_sort(numbers: List[float]) -> Dict[str, Any]:
    arr = list(numbers)
    steps: List[List[float]] = []

    def merge(left: int, mid: int, right: int) -> None:
        left_part = arr[left : mid + 1]
        right_part = arr[mid + 1 : right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            steps.append(arr.copy())
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
            steps.append(arr.copy())

        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
            steps.append(arr.copy())

    def _merge_sort(left: int, right: int) -> None:
        if left >= right:
            return
        mid = (left + right) // 2
        _merge_sort(left, mid)
        _merge_sort(mid + 1, right)
        merge(left, mid, right)

    _merge_sort(0, len(arr) - 1)
    return {"sorted": arr, "steps": steps}


def quick_sort(numbers: List[float]) -> Dict[str, Any]:
    arr = list(numbers)
    steps: List[List[float]] = []

    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                if i != j:
                    steps.append(arr.copy())
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        if i != high:
            steps.append(arr.copy())
        return i

    def _quick_sort(low: int, high: int) -> None:
        if low < high:
            pi = partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    _quick_sort(0, len(arr) - 1)
    return {"sorted": arr, "steps": steps}
