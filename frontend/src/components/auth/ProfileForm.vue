<template>
  <form @submit.prevent="saveProfile" class="form-container">
    <div class="gender-preview">
      <img :src="genderImage" alt="성별 이미지" />
    </div>

    <div v-for="(label, key) in inputFields" :key="key" class="field-group">
      <div class="field">
        <label class="field-label">{{ label }} <span class="required-dot">*</span></label>
        <BaseInput 
          type="number" 
          v-model.number="profile[key]" 
          :placeholder="`${label}를 입력하세요`"
          :class="{ 'input-error': errors[key] }"
          @input="clearError(key)"
        />
        <Transition name="fade">
          <p v-if="errors[key]" class="error-msg">{{ errors[key] }}</p>
        </Transition>
      </div>
    </div>

    <div class="field">
      <label class="field-label">성별 <span class="required-dot">*</span></label>
      <select v-model="profile.gender" class="select-field">
        <option value="M">남</option>
        <option value="F">여</option>
      </select>
    </div>

    <div class="field">
      <label class="field-label">알레르기 정보 (선택)</label>
      <textarea
        v-model="profile.allergies"
        class="textarea-field"
        placeholder="예: 땅콩, 갑각류 등 (없으면 비워두세요)"
        rows="3"
      ></textarea>
      <p class="helper-text">알레르기는 입력하지 않아도 저장이 가능합니다.</p>
    </div>

    <BaseButton :disabled="isLoading" class="submit-btn">
      <span v-if="!isLoading">내 정보 저장하기</span>
      <span v-else>저장 중...</span>
    </BaseButton>
  </form>
</template>

<script setup>
import { reactive, ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import axios from "axios"
import BaseInput from "@/components/common/BaseInput.vue"
import BaseButton from "@/components/common/BaseButton.vue"

const emit = defineEmits(['saved'])

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)

// 1. 검증에 사용할 라벨 및 범위 설정
const inputFields = {
  height: "키 (cm)",
  current_weight: "현재 체중 (kg)",
  target_weight: "목표 체중 (kg)",
  muscle_mass: "근육량 (kg)",
  body_fat: "체지방률 (%)",
  age: "나이"
}

// 프론트엔드 검증 규칙 (백엔드 모델과 동기화)
const validationRules = {
  height: { min: 50, max: 250 },
  current_weight: { min: 20, max: 300 },
  target_weight: { min: 20, max: 300 },
  muscle_mass: { min: 5, max: 150 },
  body_fat: { min: 1, max: 70 },
  age: { min: 1, max: 120 }
}

const profile = reactive({
  height: null, current_weight: null, target_weight: null,
  muscle_mass: null, body_fat: null, age: null,
  gender: "M", allergies: "",
})

const errors = reactive({
  height: "", current_weight: "", target_weight: "",
  muscle_mass: "", body_fat: "", age: "",
})

const clearError = (field) => { errors[field] = "" }

const genderImage = computed(() => {
  return profile.gender === "F"
    ? new URL("@/assets/ssafy_woman.png", import.meta.url).href
    : new URL("@/assets/ssafy_man.png", import.meta.url).href
})

const saveProfile = async () => {
  // 1. 프론트엔드 검증 로직 통일
  Object.keys(errors).forEach(key => errors[key] = "")
  let hasError = false
  
  Object.keys(validationRules).forEach(key => {
    const value = profile[key]
    const rule = validationRules[key]
    const label = inputFields[key].split(" ")[0] // 단위 제외한 라벨명

    // 빈 값 체크
    if (value === null || value === undefined || value === "") {
      errors[key] = `${label} 정보를 입력해주세요.`
      hasError = true
    } 
    // 범위 체크 (음수 및 최대치 통합 관리)
    else if (value < rule.min || value > rule.max) {
      errors[key] = `${label} 정보가 올바르지 않습니다. (${rule.min}~${rule.max} 사이)`
      hasError = true
    }
  })

  if (hasError) return

  const accessToken = localStorage.getItem("accessToken") || localStorage.getItem("access")
  if (!accessToken) {
    alert("로그인이 필요합니다.")
    router.push("/login")
    return
  }

  isLoading.value = true
  try {
    const response = await axios.put(
      "http://localhost:8000/api/accounts/me/update/",
      {
        ...profile,
        allergies: profile.allergies ? profile.allergies.trim() : ""
      },
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    
    authStore.user = response.data 
    localStorage.setItem("user", JSON.stringify(response.data))
    
    emit('saved')
    alert("건강 프로필 작성이 완료되었습니다! 🥗")
    router.replace("/")

  } catch (err) {
    const data = err.response?.data
    if (data && err.response?.status === 400) {
      // 서버 에러가 발생하더라도 위와 동일한 에러 객체에 바인딩
      Object.entries(data).forEach(([field, messages]) => {
        if (errors.hasOwnProperty(field)) {
          errors[field] = Array.isArray(messages) ? messages[0] : messages
        }
      })
    } else {
      alert("정보 저장 중 문제가 발생했습니다.")
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.form-container { display: flex; flex-direction: column; gap: 16px; width: 100%; }
.gender-preview { display: flex; justify-content: center; margin-bottom: 10px; }
.gender-preview img { width: 110px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 14px; font-weight: 700; color: #374151; }
.required-dot { color: #ef4444; margin-left: 2px; }
.error-msg { color: #ef4444; font-size: 12px; font-weight: 600; margin-top: 2px; }

:deep(.input-error) input { 
  border-color: #ef4444 !important; 
  background-color: #fffafb; 
}

.helper-text { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.select-field, .textarea-field {
  padding: 12px; border-radius: 12px; border: 1.5px solid #e2e8f0; font-size: 15px; transition: all 0.2s;
  background-color: #fff;
}
.select-field:focus, .textarea-field:focus { outline: none; border-color: #22c55e; box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.08); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.submit-btn { margin-top: 10px; }
</style>