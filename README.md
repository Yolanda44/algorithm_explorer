# Algorithm Explorer: Interactive Visualization of Sorting and Searching Algorithms

## Overview
Algorithm Explorer is a web-based teaching tool that visualizes classic sorting and searching algorithms. Students enter their own numbers, choose an algorithm, and watch every comparison and swap unfold as an animation. By exposing the internal steps—not just the final answer—the project helps younger learners and CS students build intuition about control flow, data movement, and complexity. The system pairs a Python (FastAPI) backend for rigorous algorithm execution with a lightweight HTML/JavaScript frontend for interactive visualization. The codebase demonstrates solid Python engineering (clear modules, type-safe endpoints, and reproducible environments) while delivering an approachable educational web application.

## Motivation & Objectives
- Create a hands-on teaching aid for foundational algorithms that students can explore without local setup headaches.
- Improve intuition through step-by-step animations that reveal how data moves during sorting and how indices are checked during searching.
- Encourage critical thinking about algorithm design, performance trade-offs, and time/space complexity.
- Showcase full-stack proficiency: modular Python algorithms, FastAPI endpoints, and a responsive frontend that consumes the API.
- Offer a reusable resource for instructors, mentors, and self-learners that fits lectures, workshops, or office hours.
- Model best practices (clean separation of concerns, typed request models, reproducible requirements) that professors value in student work.

## Features
**Sorting Algorithms**
- Bubble Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Captures array snapshots after each swap/merge placement
- Visual bar animations highlight changed indices

**Searching Algorithms**
- Linear Search
- Binary Search
- Recursive Binary Search
- Captures each “checked” index
- Highlights the active element during playback

**Platform Features**
- FastAPI backend with explicit request/response models
- Modular Python algorithm library for clarity and reuse
- Visualization-friendly API returning steps for animation
- Clean, minimal web interface that works from a static file
- Accepts custom input arrays; adjustable animation speed
- Education-oriented design: step counters, textual guides, algorithm summaries

## How It Works
The project uses a simple, transparent architecture:

- **Backend (FastAPI, Python)**  
  - `backend/algorithms/sorting.py` and `searching.py` implement algorithms and step tracking.  
  - `backend/algorithms/utils.py` maps algorithm names to functions.  
  - `backend/main.py` exposes `/sort` and `/search` endpoints with CORS enabled.  
  - Responses include both the final result and the sequence of steps for visualization.

- **Frontend (HTML/JS/CSS)**  
  - `frontend/index.html` provides inputs for numbers, algorithm selection, targets, and speed.  
  - `frontend/script.js` parses user input, calls the API, and animates steps with a configurable delay.  
  - `frontend/style.css` styles the layout, bars, highlights, and guide panels.

- **Data Flow**
```
User Input → POST /sort or /search (FastAPI)
          → Backend computes and records steps
          → JSON response {sorted/index, steps}
          → Frontend animates steps (bars or highlighted cells)
          → Student observes comparisons, swaps, and checked indices
```

## Installation & Usage
### Backend
```bash
cd algorithm-explorer/backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
The API serves at `http://localhost:8000`. Interactive docs are available at `/docs`.

### Frontend
- Quick open: double-click `frontend/index.html` in your browser.  
- Recommended (avoids CORS quirks):  
  ```bash
  cd algorithm-explorer/frontend
  python -m http.server 5500
  ```  
  Then visit `http://localhost:5500`.

## Examples
### Sorting (Quick Sort)
Request:
```json
POST /sort
{
  "numbers": [5, 2, 9, 1],
  "algorithm": "quick"
}
```
Response (abridged):
```json
{
  "sorted": [1, 2, 5, 9],
  "steps": [
    [2, 5, 9, 1],
    [2, 1, 9, 5],
    [1, 2, 9, 5],
    [1, 2, 5, 9]
  ]
}
```
The frontend renders these steps as bar movements, highlighting changed indices.

### Searching (Binary Search)
Request:
```json
POST /search
{
  "numbers": [1, 2, 3, 4, 5, 6],
  "target": 4,
  "algorithm": "binary"
}
```
Response:
```json
{
  "index": 3,
  "steps": [{"checked": 2}, {"checked": 3}]
}
```
During playback, the UI highlights index 2, then 3, illustrating the halving strategy.

## Educational Impact (for professors and mentors)
Visualization bridges the gap between theory and practice. By showing every swap or checked index, students see the mechanics behind big-O notation:
- **Complexity intuition**: Watching bubble sort’s repeated passes contrasts with merge sort’s divide-and-conquer merging. Binary search’s halving is visually obvious versus linear search’s sequential scan.
- **Mental models**: Animations convert abstract descriptions into concrete operations on arrays, reinforcing understanding of loops, conditionals, and recursion.
- **Classroom use**: Instructors can project the tool during lectures, let students run their own arrays in labs, or assign comparisons of algorithm behavior as homework.
- **Mentoring**: Tutors can use step-by-step playback to diagnose misconceptions (e.g., pivot placement, off-by-one in binary search).
- **Foundations**: Builds confidence in core CS topics—control flow, recursion, invariants—before tackling advanced subjects like graphs or dynamic programming.

## Technologies Used
- **Python**: Core language for algorithm implementations.
- **FastAPI**: Modern, typed web framework powering the API.
- **HTML/CSS**: Simple, portable UI layout and styling.
- **JavaScript**: Fetches API results and animates step sequences.
- **Algorithm Design & Implementation**: Clean, modular code capturing intermediate states for learning.

## Future Improvements
**Algorithm Additions**
- Graph algorithms: BFS, DFS, Dijkstra
- Dynamic programming: LIS, knapsack, edit distance
- Trie-based autocomplete and prefix search
- Pathfinding: A* search and heuristic comparisons

**Platform Enhancements**
- User-generated datasets and saved scenarios
- Richer speed controls and per-step explanations
- Code explanation panels showing pseudocode alongside playback
- Quiz mode with interactive challenges and scoring
- Mobile-friendly layout for phones and tablets
- One-click deployment presets (Render, Vercel, Fly.io)

## Why This Project Demonstrates Academic Excellence
- **Mastery of algorithms**: Implements multiple sorting and searching strategies with explicit step capture for pedagogy.
- **Strong Python engineering**: Clear module boundaries, typed request models, reproducible requirements, and CORS-aware APIs.
- **Full-stack mindset**: Harmonizes backend computation with frontend visualization, emphasizing data flow and user experience.
- **Educational focus**: Designed to help peers learn—step descriptions, algorithm guides, and adjustable pacing show care for pedagogy.
- **Computational thinking**: Encourages comparison of strategies, examination of complexity, and reflection on correctness, mirroring academic rigor.

## License & Acknowledgments
This project is released for educational use. Built with appreciation for the open-source communities behind FastAPI, Python, and the many educators who champion clear explanations of core computer science concepts. Feedback from professors, teaching assistants, and fellow students is warmly welcomed to keep improving the learning experience.
