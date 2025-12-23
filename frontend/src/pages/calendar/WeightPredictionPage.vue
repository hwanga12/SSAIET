<template>
  <div class="page">
    <h2>📈 체중 변화 예측</h2>

    <button @click="runPrediction" :disabled="loading">
      {{ loading ? "예측 중..." : "체중 변화 예측하기" }}
    </button>

    <p v-if="predicted !== null" class="result">
      👉 예상 체중 변화: 
      <strong :class="{ minus: predicted < 0, plus: predicted > 0 }">
        {{ predicted.toFixed(2) }} kg
      </strong>
    </p>

    <!-- 체중 변화 예측 차트 -->
    <canvas v-if="predicted !== null" ref="chartRef"></canvas>

    <!-- 목표 체중 진척도 -->
    <h2>목표 체중 진척도</h2>
    <div class="progress-container">
      <div class="progress-bar" :style="{ width: progressToTarget + '%' }"></div>
    </div>
    <p>{{ progressToTarget }}% 진행</p>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { predictWeightChange } from '@/stores/weight'
import axios from 'axios'
import Chart from 'chart.js/auto'

const predicted = ref(null);
const loading = ref(false);
const progressToTarget = ref(0); // 목표 체중 진척도
const chartRef = ref(null);
let chartInstance = null;

// 데이터 가져오기 (체중 예측 + 진척도)
const runPrediction = async () => {
  loading.value = true;

  try {
    const response = await axios.post('/meal/predict-weight/', { user_id: 1 });

    predicted.value = response.data.predicted_weight_change;
    progressToTarget.value = response.data.progress_to_target; // 진척도 업데이트

    await nextTick();
    drawChart(predicted.value);
  } catch (e) {
    alert("예측 실패");
    console.error(e);
  } finally {
    loading.value = false;
  }
};

// 예측된 체중 변화 차트 그리기
const drawChart = (value) => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(chartRef.value, {
    type: "bar",
    data: {
      labels: ["현재 → 예측"],
      datasets: [
        {
          label: "체중 변화 (kg)",
          data: [value],
          backgroundColor: value < 0 ? "#22c55e" : "#ef4444",
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};
</script>

<style scoped>
.page {
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
}

button {
  padding: 12px 20px;
  border-radius: 8px;
  border: none;
  background: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
}

.result {
  margin: 20px 0;
  font-size: 18px;
}

.minus {
  color: #22c55e;
}

.plus {
  color: #ef4444;
}

.progress-container {
  width: 100%;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 30px;
  background-color: #4caf50;
  width: 0;
  transition: width 0.5s ease;
}
</style>
