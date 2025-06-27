// static/js/aristocrat.js
async function loadPuzzle() {
  const res = await fetch(API_PREFIX + "/new-round");
  const { tokens, freqs } = await res.json();
  const container = document.getElementById("cipher");
  container.innerHTML = "";

  tokens.forEach((t, i) => {
    const wrapper = document.createElement("div");
    wrapper.className = "cipher-container";

    const letterSpan = document.createElement("span");
    letterSpan.className = "letter";
    letterSpan.textContent = t || "\u00A0";

    const freqSpan = document.createElement("span");
    freqSpan.className = "freq";
    freqSpan.textContent = freqs[i] != null ? freqs[i] : "";

    wrapper.append(letterSpan, freqSpan);
    container.appendChild(wrapper);
  });

  document.getElementById("feedback").textContent = "";
  document.getElementById("guess").value = "";
}

async function submitGuess() {
  const guess = document.getElementById("guess").value;
  const res = await fetch(API_PREFIX + "/check", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ guess })
  });
  const { correct } = await res.json();
  const fb = document.getElementById("feedback");

  if (correct) {
    fb.textContent = "✅ Correct!";
    fb.style.color = "green";
    setTimeout(loadPuzzle, 1000);
  } else {
    fb.textContent = "❌ Wrong, try again";
    fb.style.color = "red";
  }
}

async function skipGuess() {
  const res = await fetch(API_PREFIX + "/check", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ guess: "" })
  });
  const { answer } = await res.json();
  const fb = document.getElementById("feedback");
  fb.textContent = `➡️ The answer was: ${answer}`;
  fb.style.color = "#007bff";
  setTimeout(loadPuzzle, 2000);
}

window.addEventListener("DOMContentLoaded", loadPuzzle);
