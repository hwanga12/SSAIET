<template>
  <div class="edit-page">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <main class="page-container">
      <header class="page-header">
        <div class="header-icon">
          <span class="material-icons">manage_accounts</span>
        </div>
        <h1 class="page-title">프로필 <span class="highlight">수정</span></h1>
        <p class="page-subtitle">정확한 정보를 입력하면 최적의 식단을 추천해드려요.</p>
      </header>

      <div class="form-wrapper">
        <ProfileCard :user="auth.user" mode="edit">
          <div class="edit-form-section">
            <h3 class="section-title">신체 정보 상세</h3>
            
            <div class="form-grid">
              <div class="field">
                <label>이름</label>
                <input v-model="profile.name" placeholder="성함을 입력해주세요" class="custom-input" />
              </div>

              <div class="field">
                <label>나이</label>
                <input type="number" v-model.number="profile.age" class="custom-input" />
              </div>

              <div class="field">
                <label>성별</label>
                <select v-model="profile.gender" class="custom-select">
                  <option value="M">남자</option>
                  <option value="F">여자</option>
                </select>
              </div>

              <div class="field">
                <label>키 (cm)</label>
                <input type="number" v-model.number="profile.height" step="0.1" class="custom-input" />
              </div>

              <div class="field">
                <label>현재 체중 (kg)</label>
                <input type="number" v-model.number="profile.current_weight" step="0.1" class="custom-input" />
              </div>

              <div class="field">
                <label>목표 체중 (kg)</label>
                <input type="number" v-model.number="profile.target_weight" step="0.1" class="custom-input" />
              </div>

              <div class="field">
                <label>골격근량 (kg)</label>
                <input type="number" v-model.number="profile.muscle_mass" step="0.1" class="custom-input" />
              </div>

              <div class="field">
                <label>체지방률 (%)</label>
                <input type="number" v-model.number="profile.body_fat" step="0.1" class="custom-input" />
              </div>

              <div class="field full">
                <label>알레르기 정보</label>
                <input v-model="profile.allergies" placeholder="예: 견과류, 갑각류 등 (없으면 비워두세요)" class="custom-input" />
              </div>
            </div>
          </div>
        </ProfileCard>

        <div class="action-bar">
          <button class="btn-cancel" @click="goBack">취소</button>
          <button class="btn-save" @click="save">
            <span>변경사항 저장</span>
            <span class="material-icons">check_circle</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import ProfileCard from "@/components/profile/ProfileCard.vue"

const auth = useAuthStore()
const router = useRouter()

const profile = reactive({
  name: auth.user?.name || "",
  height: auth.user?.height || null,
  current_weight: auth.user?.current_weight || null,
  target_weight: auth.user?.target_weight || null,
  muscle_mass: auth.user?.muscle_mass || null,
  body_fat: auth.user?.body_fat || null,
  age: auth.user?.age || null,
  gender: auth.user?.gender || "M",
  allergies: auth.user?.allergies || "",
})

const save = async () => {
  try {
    await auth.updateProfile(profile)
    alert("건강 정보가 성공적으로 업데이트되었습니다. 🌱")
    router.push("/profile")
  } catch (error) {
    alert("저장 중 오류가 발생했습니다.")
  }
}

const goBack = () => {
  router.push("/profile")
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.edit-page {
  background-color: #fcfdfd;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* 배경 장식 */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.15;
}
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -150px; left: -150px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; right: -100px; }

.page-container {
  position: relative;
  z-index: 1;
  max-width: 850px;
  margin: 0 auto;
  padding: 60px 24px 100px;
}

.page-header {
  margin-bottom: 40px;
  text-align: center;
}

.header-icon {
  width: 60px;
  height: 60px;
  background: #f0fdf4;
  color: #22c55e;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -2px;
}

.highlight {
  color: #22c55e;
}

.page-subtitle {
  color: #64748b;
  margin-top: 10px;
  font-size: 1.1rem;
  font-weight: 500;
}

.edit-form-section {
  padding: 30px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 28px;
  padding-left: 10px;
  border-left: 4px solid #22c55e;
}

/* 폼 그리드 시스템 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field.full {
  grid-column: span 2;
}

label {
  font-size: 0.95rem;
  font-weight: 700;
  color: #475569;
  margin-left: 4px;
}

/* 입력 필드 디자인 통일 */
.custom-input, .custom-select {
  height: 52px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background-color: #ffffff;
  font-size: 1rem;
  color: #1e293b;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.custom-input:focus, .custom-select:focus {
  outline: none;
  border-color: #22c55e;
  background-color: #ffffff;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
  transform: translateY(-1px);
}

/* 버튼 영역 */
.action-bar {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 40px;
}

button {
  height: 56px;
  padding: 0 32px;
  border-radius: 16px;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-cancel {
  background-color: #f1f5f9;
  color: #64748b;
}

.btn-cancel:hover {
  background-color: #e2e8f0;
  color: #1e293b;
}

.btn-save {
  background-color: #0f172a; /* 딥 블랙 */
  color: #ffffff;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.15);
}

.btn-save:hover {
  background-color: #22c55e; /* 호버 시 그린 */
  box-shadow: 0 12px 24px rgba(34, 197, 94, 0.3);
  transform: translateY(-3px);
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .field.full {
    grid-column: span 1;
  }
  .page-title {
    font-size: 2rem;
  }
  .action-bar {
    flex-direction: column-reverse;
  }
  button {
    width: 100%;
    justify-content: center;
  }
}
</style>