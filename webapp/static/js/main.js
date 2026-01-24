/**
 * 🌧️ WeatherForecast AI - Enterprise Edition
 * Features: Prediction, Radar Chart, Explanations, Backtesting
 */

document.addEventListener("DOMContentLoaded", () => {
  // === STATE ===
  const state = {
    chart: null,
    currentMode: "predict", // 'predict' or 'backtest'
  };

  // === ELEMENTS ===
  const els = {
    form: document.getElementById("prediction-form"),
    submitBtn: document.getElementById("submit-btn"),
    resultSection: document.getElementById("result-section"),

    // Panels
    panelPredict: document.getElementById("panel-predict"),
    panelBacktest: document.getElementById("panel-backtest"),
    btnViewPredict: document.getElementById("view-predict"),
    btnViewBacktest: document.getElementById("view-backtest"),

    // Advanced Toggle
    toggleAdv: document.getElementById("toggle-advanced"),
    advFields: document.getElementById("advanced-fields"),

    // Inputs
    inputs: {
      kelembaban: document.getElementById("kelembaban_jam3"),
      sinar: document.getElementById("sinar_matahari"),
      angin: document.getElementById("kecepatan_angin"),
      awan: document.getElementById("tutupan_awan"),
      hujan: document.getElementById("curah_hujan"),
    },
    displays: {
      kelembaban: document.getElementById("val_kelembaban"),
      sinar: document.getElementById("val_sinar"),
      angin: document.getElementById("val_angin"),
      awan: document.getElementById("val_awan"),
      hujan: document.getElementById("val_hujan"),
    },

    // Historical
    histLocation: document.getElementById("hist-location"),
    histSearchBtn: document.getElementById("hist-search-btn"),
    histList: document.getElementById("hist-list"),
  };

  // === INITIALIZATION ===
  initChart();
  setupEventListeners();

  // === EVENT LISTENERS ===
  function setupEventListeners() {
    // 1. Navigation Switching
    els.btnViewPredict.addEventListener("click", () => switchMode("predict"));
    els.btnViewBacktest.addEventListener("click", () => switchMode("backtest"));

    // 2. Advanced Toggle
    els.toggleAdv.addEventListener("click", () => {
      const isHidden = els.advFields.classList.contains("hidden");
      if (isHidden) {
        els.advFields.classList.remove("hidden");
        els.toggleAdv.textContent = "Hide Advanced";
      } else {
        els.advFields.classList.add("hidden");
        els.toggleAdv.textContent = "Show Advanced";
      }
    });

    // 3. Slider Inputs (Live update values & Chart)
    Object.keys(els.inputs).forEach((key) => {
      const input = els.inputs[key];
      const display = els.displays[key];

      input.addEventListener("input", (e) => {
        const val = e.target.value;
        display.textContent = val;
        updateChartData(); // Real-time chart update
      });
    });

    // 4. Form Submit
    els.form.addEventListener("submit", async (e) => {
      e.preventDefault();
      handlePrediction();
    });

    // 5. Historical Search
    els.histSearchBtn.addEventListener("click", handleHistoricalSearch);
  }

  function switchMode(mode) {
    state.currentMode = mode;

    if (mode === "predict") {
      els.panelPredict.classList.remove("hidden");
      els.panelBacktest.classList.add("hidden");

      els.btnViewPredict.className =
        "flex-1 py-3 px-4 rounded-lg text-sm font-medium bg-zinc-800 text-white shadow-sm transition-all flex items-center justify-center gap-2";
      els.btnViewBacktest.className =
        "flex-1 py-3 px-4 rounded-lg text-sm font-medium text-zinc-400 hover:text-white transition-all flex items-center justify-center gap-2";
    } else {
      els.panelPredict.classList.add("hidden");
      els.panelBacktest.classList.remove("hidden");

      els.btnViewPredict.className =
        "flex-1 py-3 px-4 rounded-lg text-sm font-medium text-zinc-400 hover:text-white transition-all flex items-center justify-center gap-2";
      els.btnViewBacktest.className =
        "flex-1 py-3 px-4 rounded-lg text-sm font-medium bg-zinc-800 text-white shadow-sm transition-all flex items-center justify-center gap-2";
    }
  }

  // === CHART LOGIC (ApexCharts) ===
  function initChart() {
    const options = {
      series: [
        {
          name: "Current Input",
          data: [52, 53, 39, 62, 0], // Initial normalized values approx
        },
      ],
      chart: {
        height: 200,
        type: "radar",
        toolbar: { show: false },
        fontFamily: "Inter, sans-serif",
      },
      labels: ["Humidity", "Sunshine", "Wind", "Cloud", "Rain"],
      fill: {
        opacity: 0.2,
        colors: ["#3b82f6"],
      },
      stroke: {
        show: true,
        width: 2,
        colors: ["#3b82f6"],
        dashArray: 0,
      },
      markers: {
        size: 3,
        colors: ["#3b82f6"],
        strokeColors: "#fff",
        strokeWidth: 2,
      },
      yaxis: {
        show: false,
        min: 0,
        max: 100,
      },
      xaxis: {
        labels: {
          style: {
            colors: ["#a1a1aa", "#a1a1aa", "#a1a1aa", "#a1a1aa", "#a1a1aa"],
            fontSize: "10px",
            fontFamily: "Inter, sans-serif",
          },
        },
      },
      plotOptions: {
        radar: {
          polygons: {
            strokeColors: "#27272a",
            connectorColors: "#27272a",
          },
        },
      },
      tooltip: {
        theme: "dark",
      },
      grid: {
        padding: { top: 0, bottom: 0, left: 10, right: 10 },
      },
    };

    state.chart = new ApexCharts(
      document.querySelector("#mini-radar-chart"),
      options,
    );
    state.chart.render();
  }

  function updateChartData() {
    // Normalize data to 0-100 scale for radar chart visualization
    const humidity = parseFloat(els.inputs.kelembaban.value); // 0-100
    const sunshine = (parseFloat(els.inputs.sinar.value) / 14) * 100; // 0-14 -> 0-100
    const wind = Math.min(
      (parseFloat(els.inputs.angin.value) / 100) * 100,
      100,
    ); // 0-100+ -> 0-100
    const cloud = (parseFloat(els.inputs.awan.value) / 8) * 100; // 0-8 -> 0-100
    const rain = Math.min((parseFloat(els.inputs.hujan.value) / 50) * 100, 100); // 0-50+ -> 0-100

    state.chart.updateSeries([
      {
        name: "Current Input",
        data: [humidity, sunshine, wind, cloud, rain],
      },
    ]);
  }

  // === PREDICTION LOGIC ===
  async function handlePrediction() {
    setLoading(true);

    const formData = {
      kelembaban_jam3: parseFloat(els.inputs.kelembaban.value),
      sinar_matahari: parseFloat(els.inputs.sinar.value),
      kecepatan_angin: parseFloat(els.inputs.angin.value),
      tutupan_awan: parseFloat(els.inputs.awan.value),
      curah_hujan: parseFloat(els.inputs.hujan.value),
      // Advanced
      suhu_min: parseFloat(document.getElementById("suhu_min")?.value || 0),
      suhu_max: parseFloat(document.getElementById("suhu_max")?.value || 0),
    };

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();

      if (data.success) {
        renderResult(data);
      } else {
        alert("Error: " + data.error);
      }
    } catch (err) {
      console.error(err);
      alert("Connection error");
    } finally {
      setLoading(false);
    }
  }

  function renderResult(data) {
    const isRain = data.prediction === 1;
    const resultSection = document.getElementById("result-section");
    const resultText = document.getElementById("result-text");
    const probText = document.getElementById("probability-text");
    const probBar = document.getElementById("probability-bar");
    const explainList = document.getElementById("explanation-list");

    // Show section
    resultSection.classList.remove("hidden");

    // Text
    resultText.textContent = isRain
      ? "RAIN EXPECTED 🌧️"
      : "NO RAIN EXPECTED ☀️";
    resultText.className = isRain
      ? "text-3xl font-bold text-blue-400 tracking-tight"
      : "text-3xl font-bold text-emerald-400 tracking-tight";

    probText.textContent = `Probability: ${data.probability_rain}%`;

    // Bar
    setTimeout(() => {
      probBar.style.width = `${data.probability_rain}%`;
      probBar.className = `absolute top-0 left-0 h-full transition-all duration-1000 ease-out ${isRain ? "bg-blue-500" : "bg-emerald-500"}`;
    }, 100);

    // Explanations
    explainList.innerHTML = "";
    data.explanations.forEach((reason) => {
      const li = document.createElement("li");
      li.className = "flex items-start gap-2";
      li.innerHTML = `<span class="text-blue-500 mt-1">●</span> <span>${reason}</span>`;
      explainList.appendChild(li);
    });

    // Scroll
    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function setLoading(isLoading) {
    if (isLoading) {
      els.submitBtn.innerHTML = `<svg class="animate-spin h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Processing...`;
      els.submitBtn.disabled = true;
    } else {
      els.submitBtn.innerHTML = `<span>Analyze & Predict</span>`;
      els.submitBtn.disabled = false;
    }
  }

  // === HISTORICAL LOGIC ===
  async function handleHistoricalSearch() {
    const location = els.histLocation.value;
    if (!location) return alert("Please select a location");

    els.histSearchBtn.textContent = "Searching...";
    els.histList.innerHTML = ""; // Clear

    try {
      const res = await fetch("/api/historical/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location }),
      });
      const data = await res.json();

      if (data.success) {
        if (data.results.length === 0) {
          els.histList.innerHTML = `<div class="text-center py-10 text-zinc-500 text-sm">No records found for this location in sample database.</div>`;
        } else {
          data.results.forEach((record) => {
            const item = createHistoryItem(record);
            els.histList.appendChild(item);
          });
        }
      } else {
        els.histList.innerHTML = `<div class="text-center py-10 text-red-500 text-sm">Error: ${data.error}</div>`;
      }
    } catch (err) {
      console.error(err);
      alert("Search failed");
    } finally {
      els.histSearchBtn.textContent = "Search";
    }
  }

  function createHistoryItem(record) {
    const div = document.createElement("div");
    div.className =
      "bg-zinc-900 border border-zinc-800 rounded-lg p-4 flex items-center justify-between hover:border-zinc-700 transition-colors cursor-default";

    div.innerHTML = `
            <div>
                <div class="text-sm font-medium text-white">${record.date}</div>
                <div class="text-xs text-zinc-500 mt-1">
                    Temp: ${record.data.SuhuMax}°C | Hum: ${record.data.KelembabanJam3}% | Rain: ${record.data.CurahHujan}mm
                </div>
            </div>
            <div class="flex items-center gap-3">
                <div class="text-right">
                    <span class="block text-[10px] text-zinc-500 uppercase">Actual</span>
                    <span class="text-xs font-bold ${record.rain_tomorrow === "Yes" ? "text-blue-400" : "text-emerald-400"}">
                        ${record.rain_tomorrow === "Yes" ? "RAIN" : "DRY"}
                    </span>
                </div>
                <button class="test-btn bg-white text-black text-xs font-bold px-3 py-1.5 rounded hover:bg-zinc-200 transition-colors">
                    Test Model
                </button>
            </div>
        `;

    // Handle Test Click
    const btn = div.querySelector(".test-btn");
    btn.addEventListener("click", async () => {
      btn.textContent = "...";
      await testHistoricalRecord(record, div);
    });

    return div;
  }

  async function testHistoricalRecord(record, cardElement) {
    try {
      const res = await fetch("/api/historical/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          data: record.data,
          actual: record.rain_tomorrow,
        }),
      });
      const data = await res.json();

      // Show result IN the card
      if (data.success) {
        const statusColor = data.is_correct ? "text-green-500" : "text-red-500";
        const statusIcon = data.is_correct ? "✅" : "❌";

        const resultHtml = `
                    <div class="mt-3 pt-3 border-t border-zinc-800 flex justify-between items-center text-xs animate-in fade-in">
                        <div>
                            <span class="text-zinc-500">Model Prediction:</span>
                            <span class="font-bold text-white ml-1">${data.prediction === 1 ? "RAIN" : "DRY"} (${data.probability}%)</span>
                        </div>
                        <div class="font-bold ${statusColor} flex items-center gap-1">
                            ${statusIcon} ${data.is_correct ? "CORRECT" : "INCORRECT"}
                        </div>
                    </div>
                `;

        // Remove button, add result
        const btn = cardElement.querySelector(".test-btn");
        btn.parentElement.innerHTML =
          '<span class="text-xs text-zinc-500">Tested</span>';

        cardElement.firstElementChild.insertAdjacentHTML(
          "beforeend",
          resultHtml,
        );
      }
    } catch (err) {
      console.error(err);
      alert("Test failed");
    }
  }
});
