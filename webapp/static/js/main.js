/**
 * 🌧️ Prediksi Hujan Australia - Main JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const form = document.getElementById("prediction-form");
  const submitBtn = document.getElementById("submit-btn");
  const resultSection = document.getElementById("result-section");
  const resetBtn = document.getElementById("reset-btn");
  const modeBtns = document.querySelectorAll(".mode-btn");
  const simpleFields = document.querySelector(".simple-fields");
  const advancedFields = document.querySelector(".advanced-fields");
  const sliders = document.querySelectorAll(".slider");
  const toggleInput = document.getElementById("hujan_hari_ini");
  const toggleLabel = document.querySelector(".toggle-label");

  // Mode Toggle
  modeBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      modeBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");

      const mode = this.dataset.mode;
      if (mode === "advanced") {
        advancedFields.classList.remove("hidden");
      } else {
        advancedFields.classList.add("hidden");
      }
    });
  });

  // Slider sync with input
  sliders.forEach((slider) => {
    const targetId = slider.dataset.target;
    const targetInput = document.getElementById(targetId);

    if (targetInput) {
      // Sync slider to input
      slider.addEventListener("input", function () {
        targetInput.value = this.value;
      });

      // Sync input to slider
      targetInput.addEventListener("input", function () {
        slider.value = this.value;
      });
    }
  });

  // Toggle label update
  if (toggleInput && toggleLabel) {
    toggleInput.addEventListener("change", function () {
      toggleLabel.textContent = this.checked ? "Ya" : "Tidak";
    });
  }

  // Form Submit
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Show loading state
    submitBtn.classList.add("loading");
    submitBtn.querySelector(".btn-text").textContent = "Memprediksi...";
    submitBtn.querySelector(".btn-loader").classList.remove("hidden");
    submitBtn.querySelector(".btn-icon").classList.add("hidden");

    // Collect form data
    const formData = {
      kelembaban_jam3: parseFloat(
        document.getElementById("kelembaban_jam3").value,
      ),
      sinar_matahari: parseFloat(
        document.getElementById("sinar_matahari").value,
      ),
      kecepatan_angin: parseFloat(
        document.getElementById("kecepatan_angin").value,
      ),
      tutupan_awan: parseFloat(document.getElementById("tutupan_awan").value),
      curah_hujan: parseFloat(document.getElementById("curah_hujan").value),
    };

    // Add advanced fields if visible
    if (!advancedFields.classList.contains("hidden")) {
      formData.suhu_min = parseFloat(document.getElementById("suhu_min").value);
      formData.suhu_max = parseFloat(document.getElementById("suhu_max").value);
      formData.kelembaban_jam9 = parseFloat(
        document.getElementById("kelembaban_jam9").value,
      );
      formData.hujan_hari_ini =
        document.getElementById("hujan_hari_ini").checked;
    }

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (result.success) {
        showResult(result);
      } else {
        showError(result.error || "Terjadi kesalahan saat prediksi.");
      }
    } catch (error) {
      console.error("Error:", error);
      showError(
        "Tidak dapat terhubung ke server. Pastikan server Flask berjalan.",
      );
    } finally {
      // Reset button state
      submitBtn.classList.remove("loading");
      submitBtn.querySelector(".btn-text").textContent = "Prediksi Sekarang";
      submitBtn.querySelector(".btn-loader").classList.add("hidden");
      submitBtn.querySelector(".btn-icon").classList.remove("hidden");
    }
  });

  // Show Result
  function showResult(result) {
    const isRain = result.prediction === 1;

    // Update icon
    document.getElementById("result-icon").textContent = isRain ? "🌧️" : "☀️";

    // Update title
    document.getElementById("result-title").textContent = "Hasil Prediksi";

    // Update value with animation
    const resultValue = document.getElementById("result-value");
    resultValue.textContent = result.result;
    resultValue.className = "result-value " + (isRain ? "rain" : "no-rain");

    // Update probability
    document.getElementById("probability-value").textContent =
      result.probability_rain + "%";

    // Animate probability bar
    setTimeout(() => {
      document.getElementById("probability-fill").style.width =
        result.probability_rain + "%";
    }, 100);

    // Update input summary
    const summaryContainer = document.getElementById("input-summary");
    summaryContainer.innerHTML = "";

    for (const [label, value] of Object.entries(result.input_summary)) {
      const item = document.createElement("div");
      item.className = "summary-item";
      item.innerHTML = `
                <span class="label">${label}</span>
                <span class="value">${value}</span>
            `;
      summaryContainer.appendChild(item);
    }

    // Show result section
    resultSection.classList.remove("hidden");

    // Scroll to result
    resultSection.scrollIntoView({ behavior: "smooth", block: "center" });

    // Add rain animation if prediction is rain
    if (isRain) {
      createRainAnimation();
    } else {
      removeRainAnimation();
    }
  }

  // Show Error
  function showError(message) {
    alert("❌ Error: " + message);
  }

  // Reset Button
  resetBtn.addEventListener("click", function () {
    resultSection.classList.add("hidden");
    document.getElementById("probability-fill").style.width = "0%";
    removeRainAnimation();

    // Scroll back to form
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  // Rain Animation
  function createRainAnimation() {
    // Remove existing rain
    removeRainAnimation();

    const rainContainer = document.createElement("div");
    rainContainer.className = "rain-animation";
    rainContainer.id = "rain-container";

    // Create raindrops
    for (let i = 0; i < 100; i++) {
      const drop = document.createElement("div");
      drop.className = "raindrop";
      drop.style.left = Math.random() * 100 + "%";
      drop.style.animationDuration = Math.random() * 0.5 + 0.5 + "s";
      drop.style.animationDelay = Math.random() * 2 + "s";
      rainContainer.appendChild(drop);
    }

    document.body.appendChild(rainContainer);

    // Remove after 5 seconds
    setTimeout(() => {
      removeRainAnimation();
    }, 5000);
  }

  function removeRainAnimation() {
    const existing = document.getElementById("rain-container");
    if (existing) {
      existing.remove();
    }
  }

  // Number input validation
  document.querySelectorAll('input[type="number"]').forEach((input) => {
    input.addEventListener("input", function () {
      const min = parseFloat(this.min);
      const max = parseFloat(this.max);
      let value = parseFloat(this.value);

      if (!isNaN(min) && value < min) {
        this.value = min;
      }
      if (!isNaN(max) && value > max) {
        this.value = max;
      }
    });
  });

  console.log("🌧️ Prediksi Hujan Australia - Ready!");
});
