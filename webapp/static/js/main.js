/**
 * 🌧️ Weather Prediction AI - Client Logic
 * Modern Clean Implementation
 */

document.addEventListener("DOMContentLoaded", () => {
  // === DOM Elements ===
  const elements = {
    form: document.getElementById("prediction-form"),
    submitBtn: document.getElementById("submit-btn"),
    resultSection: document.getElementById("result-section"),
    resultText: document.getElementById("result-text"),
    probText: document.getElementById("probability-text"),
    probBar: document.getElementById("probability-bar"),
    resetBtn: document.getElementById("reset-btn"),
    modeBtns: document.querySelectorAll(".mode-btn"),
    advancedFields: document.querySelector(".advanced-fields"),
    simpleFields: document.querySelector(".simple-fields"),

    // Inputs & Value Displays
    inputs: {
      kelembaban_jam3: document.getElementById("kelembaban_jam3"),
      sinar_matahari: document.getElementById("sinar_matahari"),
      kecepatan_angin: document.getElementById("kecepatan_angin"),
      tutupan_awan: document.getElementById("tutupan_awan"),
      curah_hujan: document.getElementById("curah_hujan"),
    },
    displays: {
      kelembaban: document.getElementById("val_kelembaban"),
      sinar: document.getElementById("val_sinar"),
      angin: document.getElementById("val_angin"),
      awan: document.getElementById("val_awan"),
      hujan: document.getElementById("val_hujan"),
    },
  };

  // === Event Listeners ===

  // Slider Value Updates
  Object.keys(elements.inputs).forEach((key) => {
    elements.inputs[key].addEventListener("input", (e) => {
      if (
        elements.displays[
          key
            .replace("_jam3", "")
            .replace("_matahari", "")
            .replace("kecepatan_", "")
            .replace("tutupan_", "")
            .replace("curah_", "")
        ]
      ) {
        // Try to match shorthand keys
        const shortKey = key.split("_")[1] || key.split("_")[0]; // simple hack for mapping

        // Better mapping
        let displayEl;
        if (key === "kelembaban_jam3") displayEl = elements.displays.kelembaban;
        if (key === "sinar_matahari") displayEl = elements.displays.sinar;
        if (key === "kecepatan_angin") displayEl = elements.displays.angin;
        if (key === "tutupan_awan") displayEl = elements.displays.awan;
        if (key === "curah_hujan") displayEl = elements.displays.hujan;

        if (displayEl) displayEl.textContent = e.target.value;
      }
    });
  });

  // Mode Switching
  elements.modeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;

      // UI Toggle
      elements.modeBtns.forEach((b) => {
        b.classList.remove("bg-zinc-800", "text-white", "shadow-sm");
        b.classList.add("text-zinc-400");
      });
      btn.classList.add("bg-zinc-800", "text-white", "shadow-sm");
      btn.classList.remove("text-zinc-400");

      // Visibility
      if (mode === "advanced") {
        elements.advancedFields.classList.remove("hidden");
      } else {
        elements.advancedFields.classList.add("hidden");
      }
    });
  });

  // Form Submission
  elements.form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = {
      kelembaban_jam3: parseFloat(elements.inputs.kelembaban_jam3.value),
      sinar_matahari: parseFloat(elements.inputs.sinar_matahari.value),
      kecepatan_angin: parseFloat(elements.inputs.kecepatan_angin.value),
      tutupan_awan: parseFloat(elements.inputs.tutupan_awan.value),
      curah_hujan: parseFloat(elements.inputs.curah_hujan.value),
      // Advanced optional
      suhu_min: parseFloat(document.getElementById("suhu_min")?.value || 0),
      suhu_max: parseFloat(document.getElementById("suhu_max")?.value || 0),
      kelembaban_jam9: parseFloat(
        document.getElementById("kelembaban_jam9")?.value || 0,
      ),
      hujan_hari_ini:
        document.getElementById("hujan_hari_ini")?.checked || false,
    };

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (result.success) {
        displayResult(result);
      } else {
        alert("Error: " + result.error);
      }
    } catch (err) {
      console.error(err);
      alert("Connection failed.");
    } finally {
      setLoading(false);
    }
  });

  // Reset
  elements.resetBtn.addEventListener("click", () => {
    elements.resultSection.classList.add("hidden");
    elements.form.classList.remove("opacity-50", "pointer-events-none");
    // Reset bar width for animation next time
    elements.probBar.style.width = "0%";
  });

  // === Helper Functions ===

  function setLoading(isLoading) {
    if (isLoading) {
      elements.submitBtn.disabled = true;
      elements.submitBtn.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
            `;
    } else {
      elements.submitBtn.disabled = false;
      elements.submitBtn.innerHTML = `
                <span>Run Prediction</span>
                <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            `;
    }
  }

  function displayResult(data) {
    const isRain = data.prediction === 1;
    const probability = data.probability_rain;

    elements.resultText.textContent = isRain
      ? "Rain Predicted 🌧️"
      : "No Rain Expectation ☀️";
    elements.resultText.className = isRain
      ? "text-3xl font-bold text-blue-400 tracking-tight"
      : "text-3xl font-bold text-emerald-400 tracking-tight";

    elements.probText.textContent = `Confidence Level: ${probability.toFixed(1)}%`;

    // Show section
    elements.resultSection.classList.remove("hidden");

    // Animate Bar
    setTimeout(() => {
      elements.probBar.style.width = `${probability}%`;
      elements.probBar.className = `absolute top-0 left-0 h-full transition-all duration-1000 ease-out ${isRain ? "bg-blue-500" : "bg-emerald-500"}`;
    }, 100);

    // Scroll to result
    elements.resultSection.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }
});
