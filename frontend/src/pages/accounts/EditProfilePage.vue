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
                <label>이름 <span class="required-dot">*</span></label>
                <input v-model="profile.name" placeholder="성함을 입력해주세요" class="custom-input" :class="{ 'input-error': errors.name }" @input="errors.name = ''" />
                <p v-if="errors.name" class="error-msg">{{ errors.name }}</p>
              </div>

              <div class="field">
                <label>나이 <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.age" class="custom-input" :class="{ 'input-error': errors.age }" @input="errors.age = ''" />
                <p v-if="errors.age" class="error-msg">{{ errors.age }}</p>
              </div>

              <div class="field">
                <label>성별 <span class="required-dot">*</span></label>
                <select v-model="profile.gender" class="custom-select">
                  <option value="M">남자</option>
                  <option value="F">여자</option>
                </select>
              </div>

              <div class="field">
                <label>키 (cm) <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.height" step="0.1" class="custom-input" :class="{ 'input-error': errors.height }" @input="errors.height = ''" />
                <p v-if="errors.height" class="error-msg">{{ errors.height }}</p>
              </div>

              <div class="field">
                <label>현재 체중 (kg) <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.current_weight" step="0.1" class="custom-input" :class="{ 'input-error': errors.current_weight }" @input="errors.current_weight = ''" />
                <p v-if="errors.current_weight" class="error-msg">{{ errors.current_weight }}</p>
              </div>

              <div class="field">
                <label>목표 체중 (kg) <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.target_weight" step="0.1" class="custom-input" :class="{ 'input-error': errors.target_weight }" @input="errors.target_weight = ''" />
                <p v-if="errors.target_weight" class="error-msg">{{ errors.target_weight }}</p>
              </div>

              <div class="field">
                <label>골격근량 (kg) <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.muscle_mass" step="0.1" class="custom-input" :class="{ 'input-error': errors.muscle_mass }" @input="errors.muscle_mass = ''" />
                <p v-if="errors.muscle_mass" class="error-msg">{{ errors.muscle_mass }}</p>
              </div>

              <div class="field">
                <label>체지방률 (%) <span class="required-dot">*</span></label>
                <input type="number" v-model.number="profile.body_fat" step="0.1" class="custom-input" :class="{ 'input-error': errors.body_fat }" @input="errors.body_fat = ''" />
                <p v-if="errors.body_fat" class="error-msg">{{ errors.body_fat }}</p>
              </div>

              <div class="field full">
                <label>알레르기 정보 (선택)</label>
                <input v-model="profile.allergies" placeholder="예: 견과류, 갑각류 등 (없으면 비워두세요)" class="custom-input" />
                <p class="helper-text">알레르기는 입력하지 않아도 저장이 가능합니다.</p>
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

// 에러 메시지 상태
const errors = reactive({
  name: "",
  height: "",
  current_weight: "",
  target_weight: "",
  muscle_mass: "",
  body_fat: "",
  age: "",
})

// 검증 규칙 통일
const validationRules = {
  name: { label: "이름" },
  height: { min: 50, max: 250, label: "키" },
  current_weight: { min: 20, max: 300, label: "현재 체중" },
  target_weight: { min: 20, max: 300, label: "목표 체중" },
  muscle_mass: { min: 5, max: 150, label: "근육량" },
  body_fat: { min: 1, max: 70, label: "체지방률" },
  age: { min: 1, max: 120, label: "나이" }
}

const save = async () => {
  // 1. 에러 초기화
  Object.keys(errors).forEach(key => errors[key] = "")
  let hasError = false

  // 2. 프론트엔드 유효성 검사
  Object.keys(validationRules).forEach(key => {
    const value = profile[key]
    const rule = validationRules[key]

    if (value === null || value === undefined || value === "") {
      errors[key] = `${rule.label} 정보를 입력해주세요.`
      hasError = true
    } else if (rule.min !== undefined && (value < rule.min || value > rule.max)) {
      errors[key] = `${rule.label} 정보가 올바르지 않습니다. (${rule.min}~${rule.max} 사이)`
      hasError = true
    }
  })

  if (hasError) return

  try {
    await auth.updateProfile({
      ...profile,
      allergies: profile.allergies ? profile.allergies.trim() : ""
    })
    alert("건강 정보가 성공적으로 업데이트되었습니다. 🌱")
    router.push("/profile")
  } catch (error) {
    const data = error.response?.data
    if (data && error.response?.status === 400) {
      Object.entries(data).forEach(([field, messages]) => {
        if (errors.hasOwnProperty(field)) {
          errors[field] = Array.isArray(messages) ? messages[0] : messages
        }
      })
    } else {
      alert("저장 중 오류가 발생했습니다.")
      
    }
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
  /* 부모 차원의 스크롤만 허용 */
  overflow-y: visible; 
}

/* 배경 장식 및 컨테이너 (기존 유지) */
.bg-decoration { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.15; }
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -150px; left: -150px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; right: -100px; }

.page-container { 
  position: relative; 
  z-index: 1; 
  max-width: 850px; 
  margin: 0 auto; 
  padding: 120px 24px 100px; /* Navbar 고정 고려 상단 패딩 증가 */
}

/* ⭐ [핵심] 이중 스크롤 해결: 자식 컴포넌트(ProfileCard) 내부 스크롤 차단 */
.form-wrapper :deep(.profile-card-content),
.form-wrapper :deep(.body-info-section),
.form-wrapper :deep(section) {
  height: auto !important;
  max-height: none !important;
  overflow: visible !important;
}

/* Navbar 고정 스타일 */
.nav-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

/* 이하 기존 스타일과 동일... */
.page-header { margin-bottom: 40px; text-align: center; }
.header-icon { width: 60px; height: 60px; background: #f0fdf4; color: #22c55e; border-radius: 18px; display: flex; align-items: center; justify-content: center; margin: 24px auto 16px; }
.page-title { font-size: 2.5rem; font-weight: 900; color: #0f172a; letter-spacing: -2px; }
.highlight { color: #22c55e; }
.page-subtitle { color: #64748b; margin-top: 10px; font-size: 1.1rem; font-weight: 500; }

.edit-form-section { padding: 30px; }
.section-title { font-size: 1.2rem; font-weight: 800; color: #1e293b; margin-bottom: 28px; padding-left: 10px; border-left: 4px solid #22c55e; }

.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.field { display: flex; flex-direction: column; gap: 8px; }
.field.full { grid-column: span 2; }

label { font-size: 0.95rem; font-weight: 700; color: #475569; margin-left: 4px; }
.required-dot { color: #ef4444; margin-left: 2px; }

.custom-input, .custom-select {
  height: 52px; padding: 0 16px; border-radius: 14px; border: 1.5px solid #e2e8f0;
  background-color: #ffffff; font-size: 1rem; color: #1e293b; transition: all 0.2s ease;
}
.custom-input:focus, .custom-select:focus { outline: none; border-color: #22c55e; box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1); }
.input-error { border-color: #ef4444 !important; background-color: #fffafb; }

.error-msg { color: #ef4444; font-size: 12px; font-weight: 600; margin-left: 4px; margin-top: 2px; }
.helper-text { font-size: 12px; color: #94a3b8; margin-top: 4px; margin-left: 4px; }

.action-bar { display: flex; justify-content: center; gap: 16px; margin-top: 40px; }
button { height: 56px; padding: 0 32px; border-radius: 16px; font-weight: 800; font-size: 1rem; cursor: pointer; border: none; display: flex; align-items: center; gap: 10px; transition: 0.3s; }
.btn-cancel { background-color: #f1f5f9; color: #64748b; }
.btn-save { background-color: #0f172a; color: #ffffff; box-shadow: 0 10px 20px rgba(15, 23, 42, 0.15); }
.btn-save:hover { background-color: #22c55e; box-shadow: 0 12px 24px rgba(34, 197, 94, 0.3); transform: translateY(-3px); }

</style>