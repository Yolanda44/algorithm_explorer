from __future__ import annotations

import html
import re
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import streamlit as st

from backend.algorithms import utils


st.set_page_config(page_title="Algorithm Explorer", layout="wide")

ALGORITHM_OPTIONS: List[Tuple[str, str]] = [
    ("bubble", "Bubble Sort"),
    ("insertion", "Insertion Sort"),
    ("merge", "Merge Sort"),
    ("quick", "Quick Sort"),
    ("linear", "Linear Search"),
    ("binary", "Binary Search"),
    ("recursive-binary", "Recursive Binary Search"),
]

ALGORITHM_LABELS: Dict[str, str] = dict(ALGORITHM_OPTIONS)
SORTING_ALGORITHMS = {"bubble", "insertion", "merge", "quick"}
SEARCHING_ALGORITHMS = {"linear", "binary", "recursive-binary"}

ALGORITHM_META: Dict[str, Dict[str, Any]] = {
    "bubble": {
        "name": "Bubble Sort",
        "summary": "Repeatedly compare neighbors; swap when left > right. Large values drift right each pass.",
        "steps": [
            "Walk across neighbors and compare.",
            "Swap only when out of order.",
            "Repeat until all values are in ascending order.",
        ],
    },
    "insertion": {
        "name": "Insertion Sort",
        "summary": "Grow a sorted left side by inserting each new value into its correct position.",
        "steps": [
            "Pick the next value as the key.",
            "Shift larger left-side values right.",
            "Insert the key into the opened slot.",
        ],
    },
    "merge": {
        "name": "Merge Sort",
        "summary": "Split into halves, sort each half, then merge by repeatedly taking the smaller front item.",
        "steps": [
            "Recursively split the array.",
            "Compare fronts of two sorted halves.",
            "Write the next smallest value into the merged output.",
        ],
    },
    "quick": {
        "name": "Quick Sort",
        "summary": "Choose a pivot, partition values around it, then recurse on left and right partitions.",
        "steps": [
            "Select pivot (last element in this implementation).",
            "Move values <= pivot leftward during partition.",
            "Place pivot and recurse on both sides.",
        ],
    },
    "linear": {
        "name": "Linear Search",
        "summary": "Check values one by one from left to right until target is found or array ends.",
        "steps": [
            "Start from index 0.",
            "Compare current value with target.",
            "Return index on match, else continue.",
        ],
    },
    "binary": {
        "name": "Binary Search",
        "summary": "On sorted input, check middle and discard half of the range each step.",
        "steps": [
            "Track low/high bounds.",
            "Check midpoint value.",
            "Move low/high toward the half that can still contain target.",
        ],
    },
    "recursive-binary": {
        "name": "Recursive Binary Search",
        "summary": "Binary search performed recursively over shrinking low/high bounds.",
        "steps": [
            "Compute midpoint.",
            "Recurse into left or right half.",
            "Stop on match or empty range.",
        ],
    },
}

PSEUDOCODE: Dict[str, List[str]] = {
    "bubble": [
        "for pass in range(n):",
        "  for j in range(0, n-pass-1):",
        "    if arr[j] > arr[j+1]:",
        "      swap(arr[j], arr[j+1])",
        "return arr",
    ],
    "insertion": [
        "for i in range(1, n):",
        "  key = arr[i], j = i - 1",
        "  while j >= 0 and arr[j] > key:",
        "    arr[j+1] = arr[j]; j -= 1",
        "  arr[j+1] = key",
        "return arr",
    ],
    "merge": [
        "if len(arr) <= 1: return arr",
        "split array into left and right halves",
        "merge(sorted(left), sorted(right)):",
        "  compare fronts, write smaller value",
        "  copy remaining values",
        "return merged array",
    ],
    "quick": [
        "choose pivot = arr[high]",
        "partition values around pivot",
        "swap values that belong on left side",
        "place pivot in final sorted position",
        "recurse on left and right partitions",
        "return arr",
    ],
    "linear": [
        "for idx, value in enumerate(arr):",
        "  if value == target: return idx",
        "  continue scanning",
        "return -1",
    ],
    "binary": [
        "low = 0; high = len(arr) - 1",
        "while low <= high:",
        "  mid = (low + high) // 2",
        "  compare arr[mid] with target",
        "  move low/high to remaining half",
        "return -1",
    ],
    "recursive-binary": [
        "search(low, high):",
        "  if low > high: return -1",
        "  mid = (low + high) // 2",
        "  if arr[mid] == target: return mid",
        "  recurse on left or right half",
        "return search(0, len(arr)-1)",
    ],
}


def inject_theme() -> None:
    st.markdown(
        """
        <style>
            :root {
              --bg: #f3f8ff;
              --card: #ffffff;
              --soft: #eef4ff;
              --accent: #0ea5e9;
              --text: #0f172a;
              --muted: #475569;
              --border: rgba(15, 23, 42, 0.12);
              --success: #059669;
              --error: #ea580c;
            }

            .stApp {
              background:
                radial-gradient(circle at 8% 10%, rgba(56, 189, 248, 0.18), transparent 26%),
                radial-gradient(circle at 90% 2%, rgba(37, 99, 235, 0.14), transparent 30%),
                linear-gradient(180deg, #f7fbff, #eef4ff 60%, #f7fbff);
              color: var(--text);
            }

            [data-testid="stAppViewContainer"] > .main .block-container {
              max-width: 1050px;
              padding-top: 1.8rem;
              padding-bottom: 3rem;
            }

            .app-title { margin: 0; font-size: 2.5rem; color: #0b1224; }
            .app-subtitle { margin: 8px 0 16px 0; color: var(--muted); font-size: 1.1rem; }
            [data-testid="stWidgetLabel"] p { color: #334155; }

            .stTextArea textarea, .stTextInput input, [data-testid="stSlider"] > div {
              background: #ffffff !important;
              color: #0f172a !important;
              border: 1px solid var(--border) !important;
              border-radius: 12px !important;
            }

            [data-baseweb="select"] > div {
              background: linear-gradient(90deg, #0ea5e9, #2563eb) !important;
              color: #ffffff !important;
              border: none !important;
              border-radius: 12px !important;
              font-weight: 700 !important;
            }

            .stButton > button {
              background: linear-gradient(90deg, #0ea5e9, #2563eb) !important;
              color: #ffffff !important;
              border: none !important;
              border-radius: 12px !important;
              font-weight: 700 !important;
            }

            .guide, .viz-panel, .result-panel, .status-panel, .pseudo-panel, .why-panel {
              background: var(--card);
              border: 1px solid var(--border);
              border-radius: 14px;
              padding: 14px 16px;
              box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
            }

            .guide strong { color: #0369a1; }
            .guide ul { padding-left: 18px; margin: 8px 0 0 0; color: var(--muted); }
            .status-panel { margin-top: 10px; color: #334155; }
            .status-panel.success { color: var(--success); }
            .status-panel.error { color: var(--error); }
            .viz-panel h3, .result-panel h3, .pseudo-panel h3, .why-panel h3 { margin-top: 0; }

            .bars {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(16px, 1fr));
              align-items: end;
              gap: 8px;
              height: 320px;
              padding: 12px 4px 0;
            }

            .bar { background: linear-gradient(180deg, #38bdf8, #2563eb); border-radius: 8px 8px 4px 4px; position: relative; }
            .bar.highlight { background: linear-gradient(180deg, #fbbf24, #f97316); }
            .bar .bar-value { position: absolute; bottom: -24px; left: 50%; transform: translateX(-50%); font-size: 0.8rem; color: var(--muted); }

            .pointer-tags { position: absolute; top: -24px; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; }
            .pointer-tag, .cell-pointer {
              background: #2563eb;
              color: #ffffff;
              border-radius: 999px;
              padding: 1px 6px;
              font-size: 0.66rem;
              font-weight: 700;
            }

            .search-array { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
            .cell {
              background: #ffffff;
              border: 1px solid var(--border);
              padding: 8px 10px;
              border-radius: 10px;
              min-width: 64px;
              text-align: center;
            }
            .cell.range { background: #eff6ff; border-color: rgba(37, 99, 235, 0.35); }
            .cell.active { border-color: #0ea5e9; box-shadow: 0 6px 16px rgba(14, 165, 233, 0.22); }
            .cell.found { border-color: #059669; box-shadow: 0 6px 16px rgba(5, 150, 105, 0.2); }
            .cell .idx { display: block; font-size: 0.75rem; color: var(--muted); }
            .cell .val { display: block; font-weight: 700; color: #0f172a; }
            .cell-pointers { margin-top: 4px; display: flex; justify-content: center; gap: 4px; flex-wrap: wrap; }

            .step-panel {
              margin-top: 12px;
              padding: 10px 12px;
              border-radius: 12px;
              background: var(--soft);
              border: 1px solid var(--border);
            }

            .pseudo-panel ol {
              margin: 0;
              padding-left: 18px;
              font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
              font-size: 0.88rem;
              color: #334155;
            }
            .pseudo-panel li.active { background: #e0f2fe; color: #0c4a6e; font-weight: 700; border-radius: 6px; }
            .pointer-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
            .pointer-chip { background: #eff6ff; color: #1e3a8a; border: 1px solid rgba(37, 99, 235, 0.3); border-radius: 999px; padding: 3px 9px; font-size: 0.78rem; font-weight: 600; }
            .result-panel pre { margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; white-space: pre-wrap; color: #0f172a; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def format_list(values: Sequence[float]) -> str:
    return ", ".join(format_number(value) for value in values)


def parse_numbers(raw: str) -> List[float]:
    tokens = [token for token in re.split(r"[\s,]+", raw.strip()) if token]
    if not tokens:
        return []
    return [float(token) for token in tokens]


def map_pointers_to_indices(pointers: Dict[str, int]) -> Dict[int, List[str]]:
    mapped: Dict[int, List[str]] = {}
    for label, idx in pointers.items():
        mapped.setdefault(idx, []).append(label)
    return mapped


def render_guide(algorithm_key: str) -> None:
    meta = ALGORITHM_META.get(algorithm_key)
    if not meta:
        st.markdown(
            """
            <div class="guide">
              <strong>Algorithm Guide</strong>
              <div>Select an algorithm to see how it works.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    bullets = "".join(f"<li>{html.escape(step)}</li>" for step in meta["steps"])
    st.markdown(
        f"""
        <div class="guide">
          <strong>Algorithm Guide - {html.escape(meta["name"])}</strong>
          <div>{html.escape(meta["summary"])}</div>
          <ul>{bullets}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_sorting_markup(
    values: Sequence[float],
    highlight: Sequence[int],
    pointers: Dict[str, int],
    step_no: int,
    total_steps: int,
    detail: str,
) -> str:
    max_value = max((abs(value) for value in values), default=1.0) or 1.0
    bars: List[str] = []
    highlighted = set(highlight)
    pointer_map = map_pointers_to_indices(pointers)

    for idx, value in enumerate(values):
        height = int((abs(value) / max_value) * 220 + 24)
        classes = "bar highlight" if idx in highlighted else "bar"
        tags = "".join(
            f"<span class='pointer-tag'>{html.escape(label)}</span>"
            for label in pointer_map.get(idx, [])
        )
        bars.append(
            "<div class='{classes}' style='height: {height}px;'>"
            "<div class='pointer-tags'>{tags}</div>"
            "<span class='bar-value'>{value}</span>"
            "</div>".format(
                classes=classes,
                height=height,
                tags=tags,
                value=html.escape(format_number(value)),
            )
        )

    return (
        "<div class='viz-panel'><h3>Visualization</h3>"
        f"<div class='bars'>{''.join(bars)}</div>"
        "<div class='step-panel'>"
        f"<div><strong>Step {step_no} / {total_steps}</strong></div>"
        f"<div>{html.escape(detail)}</div>"
        "</div></div>"
    )


def build_search_markup(
    values: Sequence[float],
    active_idx: int,
    found_idx: int,
    pointers: Dict[str, int],
    active_range: Optional[Tuple[int, int]],
    step_no: int,
    total_steps: int,
    detail: str,
) -> str:
    cells: List[str] = []
    pointer_map = map_pointers_to_indices(pointers)

    for idx, value in enumerate(values):
        classes = ["cell"]
        if active_range is not None and active_range[0] <= idx <= active_range[1]:
            classes.append("range")
        if idx == active_idx:
            classes.append("active")
        if idx == found_idx:
            classes.append("found")
        pointer_badges = "".join(
            f"<span class='cell-pointer'>{html.escape(label)}</span>"
            for label in pointer_map.get(idx, [])
        )
        cells.append(
            "<div class='{class_name}'><span class='idx'>{idx}</span><span class='val'>{value}</span>"
            "<div class='cell-pointers'>{pointers}</div></div>".format(
                class_name=" ".join(classes),
                idx=idx,
                value=html.escape(format_number(value)),
                pointers=pointer_badges,
            )
        )

    return (
        "<div class='viz-panel'><h3>Visualization</h3>"
        f"<div class='search-array'>{''.join(cells)}</div>"
        "<div class='step-panel'>"
        f"<div><strong>Step {step_no} / {total_steps}</strong></div>"
        f"<div>{html.escape(detail)}</div>"
        "</div></div>"
    )


def build_learning_markup(
    algorithm_key: str,
    active_line: int,
    explanation: str,
    pointers: Dict[str, int],
) -> str:
    pseudocode = PSEUDOCODE.get(algorithm_key, [])
    lines = []
    for idx, line in enumerate(pseudocode, start=1):
        li_class = "active" if idx == active_line else ""
        lines.append(f"<li class='{li_class}'>{html.escape(line)}</li>")

    pointer_chips = "".join(
        f"<span class='pointer-chip'>{html.escape(name)} = {value}</span>"
        for name, value in pointers.items()
    )
    if not pointer_chips:
        pointer_chips = "<span class='pointer-chip'>No active pointer</span>"

    return (
        "<div class='pseudo-panel'><h3>Pseudocode</h3><ol>"
        f"{''.join(lines)}</ol></div>"
        "<div class='why-panel' style='margin-top:10px;'><h3>Why This Step?</h3>"
        f"<p>{html.escape(explanation)}</p><div class='pointer-row'>{pointer_chips}</div></div>"
    )


def build_sort_comparison_frames(
    algorithm_key: str,
    numbers: Sequence[float],
) -> List[Dict[str, Any]]:
    arr = list(numbers)
    frames: List[Dict[str, Any]] = []

    if algorithm_key == "bubble":
        n = len(arr)
        for pass_idx in range(n):
            for j in range(0, n - pass_idx - 1):
                left, right = arr[j], arr[j + 1]
                did_swap = left > right
                if did_swap:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                frames.append(
                    {
                        "values": arr.copy(),
                        "highlight": [j, j + 1],
                        "pointers": {"j": j, "j+1": j + 1},
                        "active_line": 4 if did_swap else 3,
                        "explanation": (
                            f"Compare arr[{j}]={format_number(left)} and arr[{j + 1}]={format_number(right)}; "
                            + ("swap because left > right." if did_swap else "no swap because left <= right.")
                        ),
                    }
                )
        return frames

    if algorithm_key == "insertion":
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                compared_idx = j
                compared_value = arr[compared_idx]
                did_shift = compared_value > key
                if did_shift:
                    arr[compared_idx + 1] = arr[compared_idx]
                    j -= 1
                    inserted = False
                    if j < 0:
                        arr[j + 1] = key
                        inserted = True
                    explanation = (
                        f"Compare arr[{compared_idx}]={format_number(compared_value)} with key={format_number(key)}; "
                        "shift right because arr[j] > key."
                    )
                    if inserted:
                        explanation += " Key inserted at index 0."
                else:
                    arr[compared_idx + 1] = key
                    explanation = (
                        f"Compare arr[{compared_idx}]={format_number(compared_value)} with key={format_number(key)}; "
                        f"stop shifting and insert key at index {compared_idx + 1}."
                    )

                frames.append(
                    {
                        "values": arr.copy(),
                        "highlight": [compared_idx, min(compared_idx + 1, len(arr) - 1)],
                        "pointers": {"j": compared_idx, "key_idx": i},
                        "active_line": 4 if did_shift else 3,
                        "explanation": explanation,
                    }
                )
                if not did_shift:
                    break
        return frames

    if algorithm_key == "merge":
        def merge(left: int, mid: int, right: int) -> None:
            left_part = arr[left : mid + 1]
            right_part = arr[mid + 1 : right + 1]
            i = 0
            j = 0
            k = left
            while i < len(left_part) and j < len(right_part):
                left_idx = left + i
                right_idx = mid + 1 + j
                left_val = left_part[i]
                right_val = right_part[j]
                if left_val <= right_val:
                    arr[k] = left_val
                    chosen = "left"
                    i += 1
                else:
                    arr[k] = right_val
                    chosen = "right"
                    j += 1
                frames.append(
                    {
                        "values": arr.copy(),
                        "highlight": [k, left_idx, right_idx],
                        "pointers": {"k": k, "L": left_idx, "R": right_idx},
                        "active_line": 4,
                        "explanation": (
                            f"Compare L={format_number(left_val)} (index {left_idx}) and R={format_number(right_val)} "
                            f"(index {right_idx}); write {chosen} value to index {k}."
                        ),
                    }
                )
                k += 1

            while i < len(left_part):
                arr[k] = left_part[i]
                i += 1
                k += 1
            while j < len(right_part):
                arr[k] = right_part[j]
                j += 1
                k += 1

        def merge_sort(left: int, right: int) -> None:
            if left >= right:
                return
            mid = (left + right) // 2
            merge_sort(left, mid)
            merge_sort(mid + 1, right)
            merge(left, mid, right)

        merge_sort(0, len(arr) - 1)
        return frames

    if algorithm_key == "quick":
        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low
            for j in range(low, high):
                current = arr[j]
                did_place = current <= pivot
                highlight = [j, high]
                if did_place:
                    if i != j:
                        arr[i], arr[j] = arr[j], arr[i]
                        highlight = [i, j]
                    i += 1
                frames.append(
                    {
                        "values": arr.copy(),
                        "highlight": highlight,
                        "pointers": {"low": low, "j": j, "i": i, "pivot": high},
                        "active_line": 3,
                        "explanation": (
                            f"Compare arr[{j}]={format_number(current)} with pivot={format_number(pivot)}; "
                            + ("value stays/moves to left partition." if did_place else "value stays in right partition.")
                        ),
                    }
                )
            if i != high:
                arr[i], arr[high] = arr[high], arr[i]
            return i

        def quick_sort(low: int, high: int) -> None:
            if low < high:
                pivot_idx = partition(low, high)
                quick_sort(low, pivot_idx - 1)
                quick_sort(pivot_idx + 1, high)

        quick_sort(0, len(arr) - 1)
        return frames

    return frames


def build_search_comparison_frames(
    algorithm_key: str,
    numbers: Sequence[float],
    target: float,
    steps: Sequence[Dict[str, int]],
) -> List[Dict[str, Any]]:
    frames: List[Dict[str, Any]] = []

    if algorithm_key == "linear":
        for step in steps:
            idx = int(step["checked"])
            value = numbers[idx]
            is_match = value == target
            frames.append(
                {
                    "active_idx": idx,
                    "found_idx": idx if is_match else -1,
                    "active_line": 2,
                    "explanation": (
                        f"Compare index {idx} (value {format_number(value)}) with target {format_number(target)}."
                        + (" Match found." if is_match else " Not a match.")
                    ),
                    "pointers": {"idx": idx},
                    "active_range": None,
                }
            )
        return frames

    low, high = 0, len(numbers) - 1
    for step in steps:
        mid = int(step["checked"])
        value = numbers[mid]
        comparison = "equal to"
        if value < target:
            comparison = "less than"
        elif value > target:
            comparison = "greater than"

        frames.append(
            {
                "active_idx": mid,
                "found_idx": mid if value == target else -1,
                "active_line": 4,
                "explanation": f"Compare arr[{mid}]={format_number(value)} with target {format_number(target)}; value is {comparison} target.",
                "pointers": {"low": low, "mid": mid, "high": high},
                "active_range": (low, high) if low <= high else None,
            }
        )

        if value == target:
            break
        if value < target:
            low = mid + 1
        else:
            high = mid - 1

    return frames


def render_sorting_result(run: Dict[str, Any]) -> None:
    algorithm_key = run["algorithm"]
    numbers: List[float] = run["numbers"]
    result: Dict[str, Any] = run["result"]
    speed_ms: int = run["speed_ms"]
    frames: List[Dict[str, Any]] = run["comparison_frames"]
    total_steps = len(frames)
    run_key = run["run_id"]

    viz_col, learn_col = st.columns([1.75, 1.25])
    with viz_col:
        viz_container = st.empty()
    with learn_col:
        learn_container = st.empty()

    if total_steps == 0:
        viz_container.markdown(
            build_sorting_markup(
                values=numbers,
                highlight=[],
                pointers={},
                step_no=0,
                total_steps=0,
                detail="No comparisons needed for this input.",
            ),
            unsafe_allow_html=True,
        )
        learn_container.markdown(
            build_learning_markup(
                algorithm_key=algorithm_key,
                active_line=len(PSEUDOCODE[algorithm_key]),
                explanation="Array size is too small for comparisons.",
                pointers={},
            ),
            unsafe_allow_html=True,
        )
    else:
        control_left, control_right = st.columns([4, 1])
        with control_left:
            step_no = st.slider("Step", min_value=1, max_value=total_steps, value=total_steps, key=f"sort_step_{run_key}")
        with control_right:
            autoplay = st.button("Play Steps", key=f"sort_play_{run_key}")

        def draw(current_step: int) -> None:
            frame = frames[current_step - 1]
            viz_container.markdown(
                build_sorting_markup(
                    values=frame["values"],
                    highlight=frame["highlight"],
                    pointers=frame["pointers"],
                    step_no=current_step,
                    total_steps=total_steps,
                    detail=frame["explanation"],
                ),
                unsafe_allow_html=True,
            )
            learn_container.markdown(
                build_learning_markup(
                    algorithm_key=algorithm_key,
                    active_line=frame["active_line"],
                    explanation=frame["explanation"],
                    pointers=frame["pointers"],
                ),
                unsafe_allow_html=True,
            )

        if autoplay:
            for idx in range(1, total_steps + 1):
                draw(idx)
                time.sleep(speed_ms / 1000)
        else:
            draw(step_no)

    result_text = f"Sorted: {format_list(result.get('sorted', []))}\nComparisons captured: {total_steps}"
    st.markdown(
        f"<div class='result-panel'><h3>Result</h3><pre>{html.escape(result_text)}</pre></div>",
        unsafe_allow_html=True,
    )


def render_searching_result(run: Dict[str, Any]) -> None:
    algorithm_key = run["algorithm"]
    numbers: List[float] = run["numbers"]
    result: Dict[str, Any] = run["result"]
    target = float(run.get("target"))
    speed_ms: int = run["speed_ms"]
    frames: List[Dict[str, Any]] = run["comparison_frames"]
    found_index = int(result.get("index", -1))
    total_steps = len(frames)
    run_key = run["run_id"]

    viz_col, learn_col = st.columns([1.75, 1.25])
    with viz_col:
        viz_container = st.empty()
    with learn_col:
        learn_container = st.empty()

    if total_steps == 0:
        viz_container.markdown(
            build_search_markup(
                values=numbers,
                active_idx=-1,
                found_idx=found_index,
                pointers={},
                active_range=None,
                step_no=0,
                total_steps=0,
                detail="No comparisons needed for this input.",
            ),
            unsafe_allow_html=True,
        )
        learn_container.markdown(
            build_learning_markup(
                algorithm_key=algorithm_key,
                active_line=len(PSEUDOCODE[algorithm_key]),
                explanation="No comparison step was executed.",
                pointers={},
            ),
            unsafe_allow_html=True,
        )
    else:
        control_left, control_right = st.columns([4, 1])
        with control_left:
            step_no = st.slider("Step", min_value=1, max_value=total_steps, value=total_steps, key=f"search_step_{run_key}")
        with control_right:
            autoplay = st.button("Play Steps", key=f"search_play_{run_key}")

        def draw(current_step: int) -> None:
            frame = frames[current_step - 1]
            viz_container.markdown(
                build_search_markup(
                    values=numbers,
                    active_idx=frame["active_idx"],
                    found_idx=frame["found_idx"],
                    pointers=frame["pointers"],
                    active_range=frame["active_range"],
                    step_no=current_step,
                    total_steps=total_steps,
                    detail=frame["explanation"],
                ),
                unsafe_allow_html=True,
            )
            learn_container.markdown(
                build_learning_markup(
                    algorithm_key=algorithm_key,
                    active_line=frame["active_line"],
                    explanation=frame["explanation"],
                    pointers=frame["pointers"],
                ),
                unsafe_allow_html=True,
            )

        if autoplay:
            for idx in range(1, total_steps + 1):
                draw(idx)
                time.sleep(speed_ms / 1000)
        else:
            draw(step_no)

    found_line = f"Found at index {found_index}" if found_index >= 0 else "Not found"
    result_text = f"{found_line}\nComparisons captured: {total_steps}\nTarget: {format_number(target)}"
    st.markdown(
        f"<div class='result-panel'><h3>Result</h3><pre>{html.escape(result_text)}</pre></div>",
        unsafe_allow_html=True,
    )


def run_algorithm(numbers: List[float], algorithm_key: str, target_text: str, speed_ms: int) -> None:
    if algorithm_key in SORTING_ALGORITHMS:
        result = utils.SORTING_ALGORITHMS[algorithm_key](numbers)
        comparison_frames = build_sort_comparison_frames(algorithm_key, numbers)
        status_message = "Sorting complete"
        status_tone = "success"
        target_value = None
    else:
        if not target_text.strip():
            raise ValueError("Enter a target for searching.")
        try:
            target_value = float(target_text.strip())
        except ValueError as exc:
            raise ValueError("Target must be a valid number.") from exc

        result = utils.SEARCHING_ALGORITHMS[algorithm_key](numbers, target_value)
        comparison_frames = build_search_comparison_frames(algorithm_key, numbers, target_value, result.get("steps", []))
        status_message = "Search complete"
        status_tone = "success"

    run_id = st.session_state.get("run_id", 0) + 1
    st.session_state.run_id = run_id
    st.session_state.latest_run = {
        "run_id": run_id,
        "numbers": numbers,
        "algorithm": algorithm_key,
        "target": target_value,
        "speed_ms": speed_ms,
        "result": result,
        "comparison_frames": comparison_frames,
    }
    st.session_state.status_message = status_message
    st.session_state.status_tone = status_tone


inject_theme()

if "latest_run" not in st.session_state:
    st.session_state.latest_run = None
if "run_id" not in st.session_state:
    st.session_state.run_id = 0
if "status_message" not in st.session_state:
    st.session_state.status_message = "Idle"
if "status_tone" not in st.session_state:
    st.session_state.status_tone = "info"

st.markdown("<h1 class='app-title'>Algorithm Explorer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='app-subtitle'>Light mode learning UI: visualize steps, track pointers, and map each frame to pseudocode.</p>",
    unsafe_allow_html=True,
)

raw_numbers = st.text_area("Numbers (comma or space separated)", value="5, 2, 7, 3", height=96, key="numbers_input")

col_algo, col_target, col_speed = st.columns([1.2, 1.2, 1.0])
with col_algo:
    algorithm = st.selectbox(
        "Algorithm",
        options=[option[0] for option in ALGORITHM_OPTIONS],
        format_func=lambda key: ALGORITHM_LABELS[key],
        key="algorithm_key",
    )
with col_target:
    target_raw = st.text_input(
        "Target (for searching)",
        placeholder="e.g. 4",
        disabled=algorithm in SORTING_ALGORITHMS,
        key="target_value",
    )
with col_speed:
    speed = st.slider("Animation speed", min_value=200, max_value=1500, value=700, step=100)

render_guide(algorithm)

if st.button("Run Algorithm", type="primary"):
    try:
        numbers_to_use = parse_numbers(raw_numbers)
        if not numbers_to_use:
            raise ValueError("Please enter at least one number.")
        run_algorithm(numbers_to_use, algorithm, target_raw, speed)
    except ValueError as exc:
        st.session_state.latest_run = None
        st.session_state.status_message = str(exc)
        st.session_state.status_tone = "error"

status_message = html.escape(st.session_state.status_message)
status_tone = st.session_state.status_tone
st.markdown(f"<div class='status-panel {status_tone}'>{status_message}</div>", unsafe_allow_html=True)

latest_run = st.session_state.latest_run
if latest_run:
    run_algorithm_key = latest_run["algorithm"]
    if run_algorithm_key in {"binary", "recursive-binary"} and latest_run["numbers"] != sorted(latest_run["numbers"]):
        st.warning("Binary search expects a sorted list.")

    if run_algorithm_key in SORTING_ALGORITHMS:
        render_sorting_result(latest_run)
    else:
        render_searching_result(latest_run)
