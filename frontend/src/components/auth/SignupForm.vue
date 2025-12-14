<template>
  <form @submit.prevent="submitSignup" class="form-container">
    <BaseInput label="이름" v-model="form.name" />
    <BaseInput label="아이디" v-model="form.username" />
    <BaseInput label="이메일" type="email" v-model="form.email" />
    <BaseInput label="비밀번호" type="password" v-model="form.password" />
    
    <BaseButton>회원가입</BaseButton>

  </form>
</template>

<script setup>
import { reactive } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth" // 👈 1. Store 임포트 (경로 확인 필요)

import BaseInput from "@/components/common/BaseInput.vue"
import BaseButton from "@/components/common/BaseButton.vue"

const router = useRouter()
const authStore = useAuthStore() // 👈 2. Store 사용 선언

const form = reactive({
  username: "",
  email: "",
  password: "",
  name:"",
})

const submitSignup = async () => {
  try {
    // 1. 회원가입 요청
    await axios.post("http://localhost:8000/api/accounts/signup/", form)

    // 🌟 2. 회원가입 성공 후, 즉시 자동 로그인 요청 (토큰 발급 및 localStorage 저장)
    const loginSuccess = await authStore.fetchAndStoreToken(
      form.username,
      form.password
    )

    if (loginSuccess) {
      alert("회원가입 완료!")
      // 3. 토큰이 저장되었으므로, 이제 프로필 설정 뷰로 이동
      router.replace("/profile-setup")
    } else {
      // 자동 로그인 실패 시 (비밀번호 오류 등)
      alert("회원가입 성공, 하지만 자동 로그인에 실패했습니다. 수동으로 로그인해주세요.")
      router.push("/login") // 로그인 페이지로 이동
    }

  } catch (err) {
    console.error(err)
    // Django의 에러 응답(400 Bad Request 등) 처리
    const errorMessage = err.response?.data?.username?.[0] || "회원가입 실패";
    alert(errorMessage)
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