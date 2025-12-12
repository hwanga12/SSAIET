<template>
  <form @submit.prevent="saveProfile" class="form-container">

    <BaseInput label="키(cm)" type="number" v-model="profile.height" />
    <BaseInput label="현재 체중(kg)" type="number" v-model="profile.current_weight" />
    <BaseInput label="목표 체중(kg)" type="number" v-model="profile.target_weight" />
    <BaseInput label="근육량(kg)" type="number" v-model="profile.muscle_mass" />
    <BaseInput label="체지방률(%)" type="number" v-model="profile.body_fat" />
    <BaseInput label="나이" type="number" v-model="profile.age" />

    <div>
      <label>성별</label>
      <select v-model="profile.gender">
        <option value="M">남</option>
        <option value="F">여</option>
      </select>
    </div>

    <div>
      <label>알러지 정보</label>
      <textarea v-model="profile.allergies" rows="3"></textarea>
    </div>

    <BaseButton>저장하기</BaseButton>

  </form>
</template>

<script setup>
import { reactive } from "vue"
import { useRouter } from "vue-router"      // 🌟 추가
import axios from "axios"

import BaseInput from "@/components/common/BaseInput.vue"
import BaseButton from "@/components/common/BaseButton.vue"

const router = useRouter()                  // 🌟 router 객체 생성

const profile = reactive({
  height: null,
  current_weight: null,
  target_weight: null,
  muscle_mass: null,
  body_fat: null,
  age: null,
  gender: "M",
  allergies: ""
})

const saveProfile = async () => {
  const accessToken = localStorage.getItem('accessToken')

  if (!accessToken) {
    alert("로그인이 필요합니다.")
    return
  }

  const config = {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }

  try {
    await axios.put(
      "http://localhost:8000/api/accounts/me/update/",
      profile,
      config
    )

    alert("프로필 저장 완료!")

    // 🌟 저장 성공하면 메인페이지로 이동
    router.replace("/")     // 🔥 여기 추가됨!

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
.form-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>