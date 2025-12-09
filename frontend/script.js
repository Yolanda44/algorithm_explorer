const API_BASE = "http://localhost:8000";
const sortingAlgorithms = ["bubble", "insertion", "merge", "quick"];
const searchingAlgorithms = ["linear", "binary", "recursive-binary"];

const numbersInput = document.getElementById("numbers");
const algorithmSelect = document.getElementById("algorithm");
const targetInput = document.getElementById("target");
const runButton = document.getElementById("run");
const statusLabel = document.getElementById("status");
const barsContainer = document.getElementById("bars");
const searchContainer = document.getElementById("search-array");
const output = document.getElementById("output");
const speedInput = document.getElementById("speed");
const speedValue = document.getElementById("speed-value");
const stepCounter = document.getElementById("step-counter");
const stepDetail = document.getElementById("step-detail");
const algorithmGuide = document.getElementById("algorithm-guide");

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const getDelayMs = () => Number(speedInput?.value || 700);

function updateSpeedLabel() {
  if (speedValue && speedInput) {
    speedValue.textContent = `${getDelayMs()}ms`;
  }
}

const algorithmMeta = {
  bubble: {
    name: "Bubble Sort",
    summary: "Repeatedly compare neighbors; swap if out of order. Largest items bubble to the end.",
    steps: [
      "Scan left to right, swapping adjacent out-of-order pairs.",
      "After each pass, the largest remaining item is at the right.",
      "Repeat on the unsorted prefix until no swaps are needed.",
    ],
  },
  insertion: {
    name: "Insertion Sort",
    summary: "Build the sorted list one item at a time by inserting into the correct spot to the left.",
    steps: [
      "Take the next element (the 'key').",
      "Shift larger elements right until the right position opens.",
      "Insert the key; repeat for the next element.",
    ],
  },
  merge: {
    name: "Merge Sort",
    summary: "Divide the array, sort halves, then merge them back in order.",
    steps: [
      "Split the array until single-element arrays remain.",
      "Merge two sorted halves by repeatedly taking the smaller front element.",
      "Each merge builds bigger sorted runs until the full array is sorted.",
    ],
  },
  quick: {
    name: "Quick Sort",
    summary: "Pick a pivot, partition so smaller go left and larger go right, then recurse on each side.",
    steps: [
      "Choose a pivot (here: last element).",
      "Partition: swap items so <= pivot end up left, > pivot right.",
      "Recursively sort left and right partitions.",
    ],
  },
  linear: {
    name: "Linear Search",
    summary: "Check each element in order until the target is found or the list ends.",
    steps: [
      "Start at the first element.",
      "Compare current element to target; move to next if not equal.",
      "Stop when target is found or the end is reached.",
    ],
  },
  binary: {
    name: "Binary Search",
    summary: "On a sorted array, repeatedly halve the search space around the midpoint.",
    steps: [
      "Check the middle element.",
      "If target is smaller, search left half; if larger, search right half.",
      "Repeat until found or the range is empty.",
    ],
  },
  "recursive-binary": {
    name: "Recursive Binary Search",
    summary: "Same as binary search but implemented recursively.",
    steps: [
      "Check the middle element.",
      "Recurse into left or right half based on comparison.",
      "Base case: range exhausted or target found.",
    ],
  },
};

function renderAlgorithmGuide(key) {
  if (!algorithmGuide) return;
  const meta = algorithmMeta[key];
  if (!meta) {
    algorithmGuide.innerHTML = `<strong>Algorithm Guide</strong><div class="guide-body">Select an algorithm to see how it works.</div>`;
    return;
  }
  const stepsList = meta.steps.map((s) => `<li>${s}</li>`).join("");
  algorithmGuide.innerHTML = `<strong>Algorithm Guide · ${meta.name}</strong><div class="guide-body">${meta.summary}</div><ul>${stepsList}</ul>`;
}

function parseNumbers(text) {
  const parts = text.split(/[\s,]+/).filter(Boolean);
  if (!parts.length) throw new Error("Please enter at least one number.");

  const numbers = parts.map((part) => {
    const value = Number(part);
    if (Number.isNaN(value)) {
      throw new Error(`Invalid number: "${part}"`);
    }
    return value;
  });
  return numbers;
}

function setStatus(message, tone = "info") {
  statusLabel.textContent = message;
  statusLabel.className = `status ${tone}`;
}

function updateStepInfo(position, total, description) {
  if (stepCounter) {
    stepCounter.textContent = `Step ${position} / ${total}`;
  }
  if (stepDetail) {
    stepDetail.textContent = description;
  }
}

function renderBars(array, highlightIndices = []) {
  barsContainer.innerHTML = "";
  if (!array.length) return;

  const max = Math.max(...array.map((n) => Math.abs(n)), 1);
  array.forEach((value, idx) => {
    const bar = document.createElement("div");
    bar.className = "bar";
    if (highlightIndices.includes(idx)) {
      bar.classList.add("highlight");
    }
    const height = (Math.abs(value) / max) * 200 + 24;
    bar.style.height = `${height}px`;
    bar.title = `Index ${idx}: ${value}`;

    const label = document.createElement("span");
    label.textContent = value;
    bar.appendChild(label);
    barsContainer.appendChild(bar);
  });
}

function renderSearchArray(array, activeIndex = -1, foundIndex = -1) {
  searchContainer.innerHTML = "";
  array.forEach((value, idx) => {
    const cell = document.createElement("div");
    cell.className = "cell";
    if (idx === activeIndex) cell.classList.add("active");
    if (idx === foundIndex) cell.classList.add("found");
    cell.innerHTML = `<span class="idx">${idx}</span><span class="val">${value}</span>`;
    searchContainer.appendChild(cell);
  });
}

function changedIndices(previous, current) {
  const indices = [];
  const length = Math.max(previous.length, current.length);
  for (let i = 0; i < length; i += 1) {
    if (previous[i] !== current[i]) {
      indices.push(i);
    }
  }
  return indices;
}

async function animateSorting(original, steps, delayMs) {
  searchContainer.innerHTML = "";
  barsContainer.style.display = "grid";

  const sequence = [original, ...(steps || [])];
  const totalSteps = sequence.length;

  for (let i = 0; i < totalSteps; i += 1) {
    const current = sequence[i];
    const previous = i === 0 ? [] : sequence[i - 1];
    const highlights = i === 0 ? [] : changedIndices(previous, current);
    renderBars(current, highlights);
    const description =
      i === 0
        ? `Start: [${current.join(", ")}]`
        : highlights.length
          ? `Placed/swapped indices ${highlights.join(", ")}`
          : "Continuing placement";
    updateStepInfo(i + 1, totalSteps, description);
    await delay(delayMs);
  }

  updateStepInfo(totalSteps, totalSteps, `Sorted: [${sequence[totalSteps - 1].join(", ")}]`);
}

async function animateSearch(array, steps, foundIndex, delayMs) {
  barsContainer.innerHTML = "";
  barsContainer.style.display = "none";
  renderSearchArray(array);

  const totalSteps = (steps?.length || 0) + 1;
  updateStepInfo(1, totalSteps, "Start scanning the array");
  await delay(delayMs);

  for (let i = 0; i < (steps || []).length; i += 1) {
    const step = steps[i];
    renderSearchArray(array, step.checked, -1);
    const value = array[step.checked];
    updateStepInfo(i + 2, totalSteps, `Checked index ${step.checked} (value: ${value})`);
    await delay(delayMs);
  }

  if (foundIndex >= 0) {
    renderSearchArray(array, -1, foundIndex);
    updateStepInfo(totalSteps, totalSteps, `Found target at index ${foundIndex}`);
  } else {
    updateStepInfo(totalSteps, totalSteps, "Target not found in array");
  }
}

async function runAlgorithm() {
  runButton.disabled = true;
  setStatus("Running...", "info");
  output.textContent = "";
  updateStepInfo(0, 0, "Preparing to run...");
  renderAlgorithmGuide(algorithmSelect.value);
  const delayMs = getDelayMs();

  try {
    const numbers = parseNumbers(numbersInput.value);
    const algorithm = algorithmSelect.value;
    const isSorting = sortingAlgorithms.includes(algorithm);
    const isSearching = searchingAlgorithms.includes(algorithm);

    if (!isSorting && !isSearching) {
      throw new Error("Select a sorting or searching algorithm.");
    }

    const payload = { numbers, algorithm };
    let endpoint = "/sort";

    if (isSearching) {
      const targetValue = targetInput.value.trim();
      if (!targetValue) throw new Error("Enter a target for searching.");
      const target = Number(targetValue);
      if (Number.isNaN(target)) throw new Error("Target must be a valid number.");
      payload.target = target;
      endpoint = "/search";
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }

    if (isSorting) {
      await animateSorting([...numbers], data.steps || [], delayMs);
      output.textContent = `Sorted: ${data.sorted?.join(", ")}\nSteps captured: ${data.steps?.length || 0}`;
      setStatus("Sorting complete", "success");
    } else {
      await animateSearch(numbers, data.steps || [], data.index, delayMs);
      const foundText = data.index >= 0 ? `Found at index ${data.index}` : "Not found";
      output.textContent = `${foundText}\nSteps captured: ${data.steps?.length || 0}`;
      setStatus("Search complete", "success");
    }
  } catch (error) {
    setStatus(error.message, "error");
    output.textContent = error.message;
  } finally {
    runButton.disabled = false;
  }
}

runButton.addEventListener("click", runAlgorithm);
if (speedInput) {
  speedInput.addEventListener("input", updateSpeedLabel);
  speedInput.addEventListener("change", updateSpeedLabel);
  updateSpeedLabel();
}
if (algorithmSelect) {
  algorithmSelect.addEventListener("change", () => renderAlgorithmGuide(algorithmSelect.value));
  renderAlgorithmGuide(algorithmSelect.value);
}
updateStepInfo(0, 0, "Select numbers and an algorithm, then click Run to start.");
