// ── State ─────────────────────────────────────────────────────────────────────
let filters = {};
let activeFilter = "";
let isDirty = false;
const maxes = { h: 179, s: 255, v: 255 };
const channels = ["h","s","v"];

// ── Boot ──────────────────────────────────────────────────────────────────────
async function boot() {
  const [fRes, aRes] = await Promise.all([
    fetch("/api/filters").then(r=>r.json()),
    fetch("/api/active_filter").then(r=>r.json())
  ]);
  filters = fRes;
  activeFilter = aRes.name;
  renderFilterList();
  renderSliders();
  renderDict();
}

// ── Filter list ───────────────────────────────────────────────────────────────
function swatchColor(name) {
  const swatches = {
    green:"#00e5a0", blue:"#38bdf8", orange:"#ff6b35",
    magenta:"#e879f9", red:"#f87171", yellow:"#fbbf24", white:"#fff"
  };
  return swatches[name] || "#888";
}

function renderFilterList() {
  const el = document.getElementById("filterList");
  el.innerHTML = "";
  for (const name of Object.keys(filters)) {
    const btn = document.createElement("button");
    btn.className = "filter-btn" + (name === activeFilter ? " active" : "");
    btn.innerHTML = `<span class="filter-swatch" style="background:${swatchColor(name)}"></span>${name}`;
    btn.onclick = () => selectFilter(name);
    el.appendChild(btn);
  }
  document.getElementById("bottomFilter").textContent = activeFilter;
}

async function selectFilter(name) {
  activeFilter = name;
  await fetch("/api/active_filter", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({name})
  });
  renderFilterList();
  renderSliders();
  renderDict();
}

// ── Sliders ───────────────────────────────────────────────────────────────────
function renderSliders() {
  if (!filters[activeFilter]) return;
  const { lower, upper } = filters[activeFilter];
  renderBound("lower", lower);
  renderBound("upper", upper);
}

function renderBound(bound, vals) {
  const container = document.getElementById(bound + "Sliders");
  container.innerHTML = "";
  channels.forEach((ch, i) => {
    const max = maxes[ch];
    const val = vals[i];
    const row = document.createElement("div");
    row.className = "slider-row";
    const pct = (val / max * 100).toFixed(1);

    row.innerHTML = `
      <span class="l${ch}">${ch.toUpperCase()}</span>
      <input type="range" class="r${ch}" min="0" max="${max}"
             value="${val}" style="--pct:${pct}%"
             id="${bound}_${ch}_range"
             oninput="syncInput('${bound}','${ch}',this.value,${max})">
      <input type="number" class="num-input" min="0" max="${max}"
             value="${val}" id="${bound}_${ch}_num"
             oninput="syncRange('${bound}','${ch}',this.value,${max})">
    `;
    container.appendChild(row);
  });
}

function syncInput(bound, ch, val, max) {
  val = Math.min(Math.max(parseInt(val)||0, 0), max);
  document.getElementById(`${bound}_${ch}_num`).value = val;
  updateSliderBg(bound, ch, val, max);
  updateFilterState();
}

function syncRange(bound, ch, val, max) {
  val = Math.min(Math.max(parseInt(val)||0, 0), max);
  const range = document.getElementById(`${bound}_${ch}_range`);
  range.value = val;
  updateSliderBg(bound, ch, val, max);
  updateFilterState();
}

function updateSliderBg(bound, ch, val, max) {
  const range = document.getElementById(`${bound}_${ch}_range`);
  range.style.setProperty("--pct", (val/max*100).toFixed(1)+"%");
}

function updateFilterState() {
  if (!filters[activeFilter]) return;
  for (const bound of ["lower","upper"]) {
    filters[activeFilter][bound] = channels.map(ch => {
      return parseInt(document.getElementById(`${bound}_${ch}_num`).value) || 0;
    });
  }
  renderDict();
  
  // Mark the state as changed so the interval knows to save it
  isDirty = true; 
}

// ── Apply ─────────────────────────────────────────────────────────────────────
async function applyFilter() {
  if (!filters[activeFilter]) return;
  
  // Send the request asynchronously (won't block your sliders!)
  await fetch(`/api/filters/${activeFilter}`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(filters[activeFilter])
  });
  
  // NOTE: I removed the showToast("Saved ✓") line here. 
  // Otherwise, it will flash a toast on your screen every 1/4 second!
}
// ── Auto-Sync Loop ────────────────────────────────────────────────────────────
// Run on a separate async timing interval every 250ms
setInterval(() => {
  if (isDirty) {
    applyFilter();
    isDirty = false;
  }
}, 250);
// ── Dict render ───────────────────────────────────────────────────────────────
function renderDict() {
  const box = document.getElementById("dictBox");
  let out = `<span class="kw">HSV_FILTERS</span> = {\n`;
  for (const [name, f] of Object.entries(filters)) {
    const l = f.lower, u = f.upper;
    const active = name === activeFilter;
    const prefix = active ? "  <b>" : "  ";
    const suffix = active ? "</b>" : "";
    out += `${prefix}<span class="str">"${name}"</span>: {${suffix}\n`;
    out += `    <span class="str">"lower"</span>: [<span class="num">${l[0]}, ${l[1]}, ${l[2]}</span>],\n`;
    out += `    <span class="str">"upper"</span>: [<span class="num">${u[0]}, ${u[1]}, ${u[2]}</span>],\n`;
    out += `  },\n`;
  }
  out += `}`;
  box.innerHTML = out;
}

// ── Pixel HSV hover ───────────────────────────────────────────────────────────
const inputImg = document.getElementById("inputImg");
const tooltip  = document.getElementById("tooltip");
let hoverTimer = null;

inputImg.addEventListener("mousemove", (e) => {
  clearTimeout(hoverTimer);
  hoverTimer = setTimeout(async () => {
    const rect = inputImg.getBoundingClientRect();
    const natW = inputImg.naturalWidth  || 640;
    const natH = inputImg.naturalHeight || 480;

    // MATH FIX: Calculate letterboxing from object-fit: contain
    const imgRatio = natW / natH;
    const boxRatio = rect.width / rect.height;
    let renderW = rect.width;
    let renderH = rect.height;
    let offsetX = 0;
    let offsetY = 0;

    if (imgRatio > boxRatio) {
      renderH = rect.width / imgRatio;
      offsetY = (rect.height - renderH) / 2;
    } else {
      renderW = rect.height * imgRatio;
      offsetX = (rect.width - renderW) / 2;
    }

    // Map coordinates only to the visible rendered image
    let px = Math.round((e.clientX - rect.left - offsetX) / renderW * natW);
    let py = Math.round((e.clientY - rect.top - offsetY)  / renderH * natH);

    // Stop if hovering over the black letterbox margins
    if (px < 0 || px >= natW || py < 0 || py >= natH) {
        tooltip.style.display = "none";
        return;
    }

    const data = await fetch(`/api/pixel_hsv?x=${px}&y=${py}`).then(r=>r.json());

    document.getElementById("hVal").textContent = data.h;
    document.getElementById("sVal").textContent = data.s;
    document.getElementById("vVal").textContent = data.v;

    document.getElementById("ttH").textContent = data.h;
    document.getElementById("ttS").textContent = data.s;
    document.getElementById("ttV").textContent = data.v;

    tooltip.style.display = "block";
    tooltip.style.left = (e.clientX + 14) + "px";
    tooltip.style.top  = (e.clientY - 10) + "px";
  }, 40); 
});

inputImg.addEventListener("mouseleave", () => {
  clearTimeout(hoverTimer);
  tooltip.style.display = "none";
});

// ── Toast ─────────────────────────────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 1800);
}

// ── Test Mode ─────────────────────────────────────────────────────────────────
let isTestMode = false;

document.getElementById("testToggle").addEventListener("click", async () => {
  isTestMode = !isTestMode;
  await fetch("/api/test_mode", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({enabled: isTestMode})
  });
  applyTestModeUI();
});

function applyTestModeUI() {
  const toggle = document.getElementById("testToggle");
  const panel  = document.getElementById("testPanel");
  const status = document.getElementById("headerStatus");

  toggle.classList.toggle("active", isTestMode);
  panel.style.display = isTestMode ? "flex" : "none";

  status.innerHTML = isTestMode
    ? `<div class="dot" style="background:var(--accent2)"></div><span style="color:var(--accent2)">Test Mode</span>`
    : `<div class="dot"></div>Pi Camera Stream`;
}

// Wire up file input (hidden, triggered by click on drop zone label)
document.getElementById("dropZoneLabel").addEventListener("click", () => {
  document.getElementById("fileInput").click();
});
document.getElementById("fileInput").addEventListener("change", (e) => {
  if (e.target.files[0]) handleFileSelect(e.target.files[0]);
});

async function handleFileSelect(file) {
  if (!file) return;
  document.getElementById("dzName").textContent = file.name;

  const formData = new FormData();
  formData.append("image", file);

  const res  = await fetch("/api/upload_test_image", {method:"POST", body: formData});
  const data = await res.json();

  if (data.ok) {
    showToast(`Loaded ${data.size[0]}×${data.size[1]} ✓`);
    isTestMode = true;
    applyTestModeUI();
    document.getElementById("testPanel").classList.add("active");
  } else {
    showToast("Upload failed ✗");
  }
}

// Drag-and-drop on the label
const dropZoneLabel = document.getElementById("dropZoneLabel");
dropZoneLabel.addEventListener("dragover",  e => { e.preventDefault(); dropZoneLabel.classList.add("over"); });
dropZoneLabel.addEventListener("dragleave", () => dropZoneLabel.classList.remove("over"));
dropZoneLabel.addEventListener("drop", e => {
  e.preventDefault();
  dropZoneLabel.classList.remove("over");
  const file = e.dataTransfer.files[0];
  if (file) handleFileSelect(file);
});

// ── Init ──────────────────────────────────────────────────────────────────────
boot();