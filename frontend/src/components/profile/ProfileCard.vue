<template>
  <section class="profile-top">
    <!-- 왼쪽: 사진 + 이름 (공통) -->
    <div class="left">
      <div class="avatar">
        <img :src="genderImage" alt="profile" />
      </div>
      <h2 class="name">{{ user.name }}</h2>
    </div>

    <!-- 오른쪽 -->
    <div class="right">
      <!-- 🔹 조회 모드 -->
      <template v-if="mode === 'view'">
        <h3 class="section-title">신체 정보</h3>

        <div class="info-grid">
          <div class="item">
            <span class="label">키</span>
            <strong class="value">
              {{ user.height }}
              <span class="unit">cm</span>
            </strong>
          </div>

          <div class="item">
            <span class="label">나이</span>
            <strong class="value">
              {{ user.age }}
              <span class="unit">세</span>
            </strong>
          </div>

          <div class="item">
            <span class="label">성별</span>
            <strong class="value">
              {{ user.gender === "M" ? "남자" : "여자" }}
            </strong>
          </div>

          <div class="item">
            <span class="label">현재 체중</span>
            <strong class="value">
              {{ user.current_weight }}
              <span class="unit">kg</span>
            </strong>
          </div>

          <div class="item">
            <span class="label">목표 체중</span>
            <strong class="value">
              {{ user.target_weight }}
              <span class="unit">kg</span>
            </strong>
          </div>

          <div class="item">
            <span class="label">체지방률</span>
            <strong class="value">
              {{ user.body_fat }}
              <span class="unit">%</span>
            </strong>
          </div>

          <div class="item">
            <span class="label">골격근량</span>
            <strong class="value">
              {{ user.muscle_mass }}
              <span class="unit">kg</span>
            </strong>
          </div>
        </div>

        <!-- 🚫 알러지 -->
        <div class="allergy-box">
          <span class="allergy-label">알러지 정보</span>
          <p class="allergy-text">
            {{ user.allergies || "등록된 알러지 정보가 없습니다." }}
          </p>
        </div>
      </template>

      <!-- 🔹 수정 모드 -->
      <template v-else>
        <slot />
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  mode: {
    type: String,
    default: "view" // view | edit
  }
})

/* 👤 성별 이미지 */
const genderImage = computed(() => {
  return props.user.gender === "F"
    ? new URL("@/assets/ssafy_woman.png", import.meta.url).href
    : new URL("@/assets/ssafy_man.png", import.meta.url).href
})
</script>

<style scoped>
/* 카드 전체 */
.profile-top {
  display: flex;
  gap: 48px;
  background: #fff;
  padding: 44px;
  border-radius: 28px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* 왼쪽 영역 */
.left {
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar {
  width: 200px;
  height: 200px;
  border-radius: 32px;
  background: linear-gradient(145deg, #f2f4f6, #ffffff);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 150px;
  height: auto;
}

.name {
  margin-top: 18px;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.3px;
}

/* 오른쪽 영역 */
.right {
  flex: 1;
}

.section-title {
  margin: 0 0 22px;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.4px;
}

/* 정보 그리드 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px 28px;
}

.item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 14px;
  color: #777;
}

.value {
  font-size: 18px;
  font-weight: 600;
}

.unit {
  margin-left: 4px;
  font-size: 14px;
  color: #777;
}

/* 알러지 */
.allergy-box {
  margin-top: 28px;
  padding-top: 18px;
  border-top: 1px solid #eee;
}

.allergy-label {
  display: block;
  font-size: 14px;
  color: #999;
  margin-bottom: 6px;
}

.allergy-text {
  font-size: 15px;
  color: #444;
}
</style>