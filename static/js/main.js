/* ═══════════════════════════════════════════════════════
   தமிழ் கற்போம் — main.js
   Speech: gTTS via Flask /speak route (free, no API key)
   ═══════════════════════════════════════════════════════ */
"use strict";

let DATA = {};

document.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  renderUyir();
  renderMei();
  renderMatrix();
  renderNumbers();
  bindTabs();
});

async function loadData() {
  const res = await fetch("/api/data");
  DATA = await res.json();
}

/* ══════════════════════════════════════════════════════
   SPEECH — Flask /speak?text=... → MP3 → Audio()
   ══════════════════════════════════════════════════════ */
let currentAudio = null;

function speak(text, btnEl) {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
    document.querySelectorAll(".speech-btn.playing")
      .forEach(b => b.classList.remove("playing"));
  }
  const url   = `/speak?text=${encodeURIComponent(text)}`;
  const audio = new Audio(url);
  currentAudio = audio;
  if (btnEl) btnEl.classList.add("playing");
  audio.play().catch(() => showToast("⚠️ Speech error — check internet connection"));
  audio.onended = () => { if (btnEl) btnEl.classList.remove("playing"); currentAudio = null; };
  audio.onerror = () => { if (btnEl) btnEl.classList.remove("playing"); currentAudio = null; showToast("⚠️ gTTS error"); };
}

function speakerSVG() {
  return `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>
  </svg>`;
}

function makeSpeechBtn(speakText) {
  const btn = document.createElement("button");
  btn.className = "speech-btn";
  btn.title = `Speak: ${speakText}`;
  btn.setAttribute("aria-label", `Pronounce ${speakText}`);
  btn.innerHTML = speakerSVG();
  btn.addEventListener("click", e => { e.stopPropagation(); speak(speakText, btn); });
  return btn;
}

/* ══════════════════════════════════════════════════════
   TAB 1 — UYIR (13 Vowels including ஃ)
   ══════════════════════════════════════════════════════ */
function renderUyir() {
  const grid = document.getElementById("grid-uyir");
  grid.innerHTML = "";
  DATA.uyir.forEach(item => {
    const card = document.createElement("div");
    card.className = "card" + (item.is_aayutham ? " aayutham-card" : "");

    const letter = el("div", "card-letter", item.ta);
    const sub    = document.createElement("div");
    sub.className = "card-sub";
    sub.innerHTML = `${item.en} <span class="ta">(${item.sub_ta})</span>`;
    const roman  = el("div", "card-roman", item.roman);
    const btn    = makeSpeechBtn(item.speak);

    card.append(letter, sub, roman, btn);
    grid.appendChild(card);
  });
}

/* ══════════════════════════════════════════════════════
   TAB 2 — MEI (18 Consonants as cards)
   ══════════════════════════════════════════════════════ */
function renderMei() {
  const grid = document.getElementById("grid-mei");
  grid.innerHTML = "";
  DATA.mei.forEach(item => {
    const card   = document.createElement("div");
    card.className = "card";
    const letter = el("div", "card-letter", item.ta);
    const sub    = document.createElement("div");
    sub.className = "card-sub";
    sub.innerHTML = `${item.en} <span class="ta">(${item.sub_ta})</span>`;
    const roman  = el("div", "card-roman", item.roman);
    const btn    = makeSpeechBtn(item.speak);
    card.append(letter, sub, roman, btn);
    grid.appendChild(card);
  });
}

/* ══════════════════════════════════════════════════════
   TAB 3 — UYIRMEI MATRIX TABLE
   Matches reference image:
   · Top row  = vowel headers  (blue bg)
   · Left col = consonant rows (green bg)
   · Cells    = alternating pink / yellow rows
   · Click any cell → gTTS speaks letter
   ══════════════════════════════════════════════════════ */
function renderMatrix() {
  const thead = document.getElementById("matrix-thead");
  const tbody = document.getElementById("matrix-tbody");
  thead.innerHTML = tbody.innerHTML = "";

  const vHeaders = DATA.vowel_headers;
  const rows     = DATA.matrix;

  /* Header row */
  const headTr = document.createElement("tr");
  const corner = document.createElement("th");
  corner.className = "corner-cell";
  corner.innerHTML = `<span style="font-size:1.4rem">ஃ</span><br><span style="font-size:0.75rem;font-weight:700">ak</span>`;
  headTr.appendChild(corner);

  vHeaders.forEach(vh => {
    const th = document.createElement("th");
    th.className = "vh-cell";
    th.innerHTML = `<div class="cell-inner"><span class="vh-ta">${vh.ta}</span><span class="vh-en">${vh.en}</span></div>`;
    headTr.appendChild(th);
  });
  thead.appendChild(headTr);

  /* Body rows */
  rows.forEach(row => {
    const tr = document.createElement("tr");

    /* Row header */
    const rh = document.createElement("td");
    rh.className = "rh-cell";
    rh.style.cursor = "pointer";
    rh.title = `Speak: ${row.mei}`;
    rh.innerHTML = `<div class="cell-inner"><span class="rh-ta">${row.mei}</span><span class="rh-en">${row.en_row}</span></div>`;
    rh.addEventListener("click", () => speak(row.speak_mei, null));
    tr.appendChild(rh);

    /* Data cells */
    row.cells.forEach(cell => {
      const td = document.createElement("td");
      td.className = "data-cell";
      td.title = `${cell.ta} — click to hear`;
      td.innerHTML = `
        <div class="cell-inner">
          <span class="cell-ta">${cell.ta}</span>
          <span class="cell-en">${cell.en}</span>
          <span class="cell-speak-icon">🔊</span>
        </div>
      `;
      td.addEventListener("click", () => speak(cell.speak, null));
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
}

/* ══════════════════════════════════════════════════════
   TAB 4 — NUMBERS
   ══════════════════════════════════════════════════════ */
function renderNumbers() {
  const grid = document.getElementById("grid-numbers");
  grid.innerHTML = "";
  DATA.numbers.forEach(item => {
    const card    = document.createElement("div");
    card.className = "card";
    const letter  = el("div", "card-letter",  item.ta);
    const numeral = el("div", "card-numeral", item.num);
    const sub     = document.createElement("div");
    sub.className = "card-sub";
    sub.innerHTML = `${item.en} <span class="ta">(${item.sub_ta})</span>`;
    const btn = makeSpeechBtn(item.speak);
    card.append(letter, numeral, sub, btn);
    grid.appendChild(card);
  });
}

/* ══════════════════════════════════════════════════════
   TABS
   ══════════════════════════════════════════════════════ */
function bindTabs() {
  const btns     = document.querySelectorAll(".tab-btn");
  const sections = document.querySelectorAll(".section");
  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      sections.forEach(s => {
        s.classList.remove("visible");
        if (s.id === `tab-${btn.dataset.tab}`) s.classList.add("visible");
      });
    });
  });
}

/* ══════════════════════════════════════════════════════
   HELPERS
   ══════════════════════════════════════════════════════ */
function el(tag, cls, text) {
  const e = document.createElement(tag);
  e.className   = cls;
  e.textContent = text;
  return e;
}

function showToast(msg, ms = 3000) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.remove("hidden");
  setTimeout(() => t.classList.add("hidden"), ms);
}
