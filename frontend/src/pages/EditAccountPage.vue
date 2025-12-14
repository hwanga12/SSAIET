<template>
  <div class="page">
    <h1>계정 수정</h1>

    <div class="form">
      <label>아이디</label>
      <input v-model="username">

      <label>이메일</label>
      <input v-model="email">

      <label>새 비밀번호</label>
      <input type="password" v-model="password">
    </div>

    <button @click="save">수정하기</button>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()

const username = ref(auth.user.username)
const email = ref(auth.user.email)
const password = ref("")  // 선택 입력

const save = async () => {
  await auth.updateAccount({
    username: username.value,
    email: email.value,
    password: password.value || undefined,
  })

  alert("계정 정보가 수정되었습니다!")
}
</script>

<style scoped>
.page { width: 330px; margin: 30px auto; }
.form { display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }
input { padding: 6px; }
button { padding: 8px; cursor: pointer; width: 100%; }
</style>