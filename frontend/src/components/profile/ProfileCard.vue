<template>
  <section class="profile-card-content">
    <div class="user-info-section">
      <div class="avatar-wrapper">
        <img :src="genderImage" alt="profile" />
      </div>
      <h2 class="user-name">{{ user.name }}</h2>
    </div>

    <div class="body-info-section">
      <template v-if="mode === 'view'">
        <div class="info-list">
          <div class="info-row">
            <span class="label">키 / 나이 / 성별</span>
            <span class="value">
              <strong>{{ user.height }}</strong>cm / 
              <strong>{{ user.age }}</strong>세 / 
              <strong>{{ user.gender === "M" ? "남" : "여" }}</strong>
            </span>
          </div>

          <div class="info-row">
            <span class="label">현재 체중</span>
            <span class="value"><strong>{{ user.current_weight }}</strong> kg</span>
          </div>

          <div class="info-row">
            <span class="label">목표 체중</span>
            <span class="value accent"><strong>{{ user.target_weight }}</strong> kg</span>
          </div>

          <div class="info-row">
            <span class="label">골격근량 / 체지방</span>
            <span class="value">
              <strong>{{ user.muscle_mass }}</strong>kg / 
              <strong>{{ user.body_fat }}</strong>%
            </span>
          </div>
        </div>

        <div class="allergy-footer">
          <span class="label">알러지 정보</span>
          <p class="text">{{ user.allergies || "등록된 정보 없음" }}</p>
        </div>

        <div class="profile-action-group">
          <button class="action-btn secondary-btn" @click="goAccountEdit">
            <span class="material-icons">manage_accounts</span>
            <span>계정 설정</span>
          </button>
          <button class="action-btn primary-btn" @click="goEdit">
            <span class="material-icons">settings</span>
            <span>내 정보 수정하기</span>
          </button>
        </div>
      </template>

      <template v-else>
        <slot />
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  user: { type: Object, required: true },
  mode: { type: String, default: "view" }
})
const router = useRouter()
const goEdit = () => router.push("/profile/edit")
const goAccountEdit = () => router.push("/account/edit")

// 부모 컴포넌트로 버튼 클릭 이벤트를 보냄
defineEmits(['account-edit', 'profile-edit'])

const genderImage = computed(() => {
  return props.user.gender === "F"
    ? new URL("@/assets/ssafy_woman.png", import.meta.url).href
    : new URL("@/assets/ssafy_man.png", import.meta.url).href
})
</script>

<style scoped>
/* 기존 스타일 유지 */
.profile-card-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  padding: 30px;
  box-sizing: border-box;
}

.user-info-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 25px;
  border-bottom: 1px dashed #f1f5f9;
  margin-bottom: 25px;
}

.avatar-wrapper {
  width: 160px;
  height: 160px;
  background: #f8fafc;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; 
  border: 1px solid #f1f5f9;
}

.avatar-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.user-name {
  margin-top: 15px;
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
}

.info-list { display: flex; flex-direction: column; gap: 16px; }
.info-row { display: flex; justify-content: space-between; align-items: center; }
.label { font-size: 0.85rem; color: #94a3b8; font-weight: 600; }
.value { font-size: 1rem; color: #334155; }
.value strong { color: #0f172a; font-weight: 800; }
.value.accent strong { color: #22c55e; }

.allergy-footer {
  margin-top: 25px;
  padding: 15px;
  background: #fcfdfd;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
}

.allergy-footer .text {
  margin-top: 5px;
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.4;
}

/* ✅ 추가된 버튼 그룹 스타일 */
.profile-action-group {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  border-radius: 16px;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.secondary-btn {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.primary-btn {
  background: #0f172a;
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.primary-btn:hover {
  background: #22c55e;
  box-shadow: 0 8px 15px rgba(34, 197, 94, 0.2);
}

.secondary-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}
</style>