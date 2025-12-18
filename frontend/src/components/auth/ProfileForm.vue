<template>
  <form @submit.prevent="saveProfile" class="form-container">

    <!-- 👤 성별 이미지 미리보기 -->
    <div class="gender-preview">
      <img :src="genderImage" alt="성별 이미지" />
    </div>

    <!-- 기본 입력 -->
    <BaseInput label="키 (cm)" type="number" v-model="profile.height" />
    <BaseInput label="현재 체중 (kg)" type="number" v-model="profile.current_weight" />
    <BaseInput label="목표 체중 (kg)" type="number" v-model="profile.target_weight" />
    <BaseInput label="근육량 (kg)" type="number" v-model="profile.muscle_mass" />
    <BaseInput label="체지방률 (%)" type="number" v-model="profile.body_fat" />
    <BaseInput label="나이" type="number" v-model="profile.age" />

    <!-- 🔽 성별 -->
    <div class="field">
      <label class="field-label">성별</label>
      <select v-model="profile.gender" class="select-field">
        <option value="M">남</option>
        <option value="F">여</option>
      </select>
    </div>

    <!-- 📝 알러지 -->
    <div class="field">
      <label class="field-label">알러지 정보</label>
      <textarea
        v-model="profile.allergies"
        class="textarea-field"
        placeholder="예: 땅콩, 갑각류, 우유 등"
        rows="3"
      ></textarea>
    </div>

    <BaseButton>저장하기</BaseButton>
  </form>
</template>

<script setup>
import { reactive, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

import BaseInput from "@/components/common/BaseInput.vue"
import BaseButton from "@/components/common/BaseButton.vue"

const router = useRouter()

const profile = reactive({
  height: null,
  current_weight: null,
  target_weight: null,
  muscle_mass: null,
  body_fat: null,
  age: null,
  gender: "M",
  allergies: "",
})

/* 👤 성별에 따른 이미지 */
const genderImage = computed(() => {
  return profile.gender === "F"
    ? new URL("@/assets/ssafy_woman.png", import.meta.url).href
    : new URL("@/assets/ssafy_man.png", import.meta.url).href
})

const saveProfile = async () => {
  const accessToken = localStorage.getItem("accessToken")
  if (!accessToken) {
    alert("로그인이 필요합니다.")
    return
  }

  try {
    await axios.put(
      "http://localhost:8000/api/accounts/me/update/",
      profile,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    alert("프로필 저장 완료!")
    router.replace("/")
  } catch (err) {
    console.error("프로필 저장 오류:", err.response || err)
    if (err.response?.status === 403) {
      alert("로그인 만료 또는 권한 없음. 다시 로그인해주세요.")
      router.push("/login")
    } else {
      alert("프로필 저장 실패.")
    }
  }
}
</script>

<style scoped>
/* 전체 폼 */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* 성별 이미지 */
.gender-preview {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}
.gender-preview img {
  width: 120px;
}

/* 공통 필드 */
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.field-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

/* select 스타일 */
.select-field {
  height: 44px;
  padding: 0 12px;
  font-size: 14px;
  color: #111827;

  border-radius: 10px;
  border: 1.5px solid #d1d5db;
  background-color: #ffffff;

  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%236b7280' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;

  transition: all 0.15s ease;
}
.select-field:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.15);
}

/* textarea 스타일 */
.textarea-field {
  min-height: 96px;
  padding: 10px 12px;

  font-size: 14px;
  line-height: 1.5;
  color: #111827;

  border-radius: 10px;
  border: 1.5px solid #d1d5db;
  resize: vertical;

  transition: all 0.15s ease;
}
.textarea-field:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.15);
}
</style>