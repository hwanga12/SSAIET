<template>
  <div class="prediction-layout">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-soft"></div>
    </div>

    <main class="prediction-page">
      <div class="container">
        <header class="page-header">
          <div class="header-left">
            <div class="icon-badge">
              <span class="material-icons">trending_down</span>
            </div>
            <div class="title-group">
              <span class="sub-title">Health Analytics</span>
              <h1>체중 <span class="highlight">변화</span> 예측</h1>
              <p>현재 식단을 유지했을 때 30일 후의 변화를 머신러닝으로 예측합니다.</p>
            </div>
          </div>

          <div class="header-right">
            <div class="summary-card">
              <div class="summary-info">
                <span class="label">목표 달성률</span>
                <span class="value">
                  <strong>{{ progress }}</strong>
                  <small>%</small>
                </span>
              </div>
              <div class="summary-icon">🎯</div>
            </div>
          </div>
        </header>

        <section class="content-section">
          <div class="glass-card prediction-trigger">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">현재 체중</span>
                <span class="info-value">{{ currentWeight || '--' }} <small>kg</small></span>
              </div>
              <div class="info-item">
                <span class="info-label">목표 체중</span>
                <span class="info-value">{{ targetWeight || '--' }} <small>kg</small></span>
              </div>
              <div class="info-item highlight-item">
                <span class="info-label">30일 후 예상</span>
                <span class="info-value">{{ predictedWeight || '--' }} <small>kg</small></span>
              </div>
            </div>
            
            <button @click="runPrediction" :disabled="loading" class="main-btn">
              <span class="material-icons">{{ loading ? 'sync' : 'psychology' }}</span>
              {{ loading ? "AI 분석 중..." : "변화 예측하기" }}
            </button>
          </div>

          <div v-if="predictedWeight" class="glass-card chart-container">
            <div class="card-header">
              <h3><span class="material-icons">insights</span> 체중 변화 추이 시뮬레이션</h3>
            </div>
            <div class="chart-wrapper">
              <canvas ref="chartRef"></canvas>
            </div>
            <div class="chart-footer">
              <p class="notice">
                * 위 예측은 최근 30일간의 평균 섭취 칼로리와 사용자의 신체 데이터를 기반으로 산출되었습니다.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import axios from "axios";
import Chart from "chart.js/auto";
import BaseNavbar from "@/components/common/BaseNavbar.vue";

/* ================= STATE ================= */
const currentWeight = ref(null);
const targetWeight = ref(null);
const predictedWeight = ref(null);
const progress = ref(0);
const loading = ref(false);

const chartRef = ref(null);
let chartInstance = null;

/* ================= METHODS ================= */
const runPrediction = async () => {
  loading.value = true;
  try {
    const res = await axios.post("/meal/predict-weight/");
    currentWeight.value = res.data.current_weight;
    targetWeight.value = res.data.target_weight;
    predictedWeight.value = res.data.predicted_weight_30d;
    progress.value = res.data.progress_to_target;

    await nextTick();
    drawChart();
  } catch (e) {
    alert("예측 데이터를 가져오는데 실패했습니다.");
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const drawChart = () => {
  if (chartInstance) chartInstance.destroy();

  const ctx = chartRef.value.getContext("2d");
  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["현재", "30일 후 (예측)", "최종 목표"],
      datasets: [{
        label: "체중 (kg)",
        data: [currentWeight.value, predictedWeight.value, targetWeight.value],
        borderColor: "#059669",
        backgroundColor: "rgba(5, 150, 105, 0.1)",
        borderWidth: 3,
        pointBackgroundColor: "#059669",
        pointRadius: 6,
        fill: true,
        tension: 0.4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: { color: "#f1f5f9" }
        },
        x: {
          grid: { display: false }
        }
      }
    },
  });
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

.prediction-layout {
  min-height: 100vh;
  background: #fcfdfd;
  position: relative;
  overflow-x: hidden;
  padding-top: 80px;
}

.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px 24px;
  position: relative;
  z-index: 1;
}

/* Header & Summary Card (식단 페이지와 동일) */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  gap: 24px;
}

.icon-badge {
  width: 52px;
  height: 52px;
  background: #064e3b;
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(6, 78, 59, 0.2);
  margin-bottom: 16px;
}

.title-group h1 {
  font-size: 2.4rem;
  font-weight: 800;
  color: #0f172a;
}

.highlight { color: #059669; }

.summary-card {
  background: white;
  padding: 24px 32px;
  border-radius: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 20px;
}

.summary-info .value {
  font-size: 2rem;
  font-weight: 800;
  color: #064e3b;
}

/* Glass Card 디자인 */
.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-radius: 32px;
  padding: 40px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.8);
  margin-bottom: 30px;
}

/* Info Grid */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  text-align: center;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 600;
}

.info-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1e293b;
}

.highlight-item .info-value {
  color: #059669;
}

/* Button */
.main-btn {
  width: 100%;
  padding: 18px;
  border-radius: 16px;
  border: none;
  background: #064e3b;
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s;
}

.main-btn:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(5, 150, 105, 0.2);
}

.main-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

/* Chart */
.chart-container h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  color: #1e293b;
}

.chart-wrapper {
  height: 350px;
  position: relative;
}

.chart-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
}

.notice {
  font-size: 0.85rem;
  color: #94a3b8;
  line-height: 1.5;
}

/* Decoration Blobs (동일 적용) */
.bg-decoration { position: fixed; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); opacity: 0.3; border-radius: 50%; }
.blob-green { width: 500px; height: 500px; background: #059669; top: -150px; right: -100px; }
.blob-soft { width: 400px; height: 400px; background: #d1fae5; bottom: -100px; left: -100px; }

@media (max-width: 768px) {
  .info-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; }
  .glass-card { padding: 24px; }
}
</style>