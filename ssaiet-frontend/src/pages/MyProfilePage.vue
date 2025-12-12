<template>
  <div class="page">
    <h1>내 프로필</h1>

    <div class="box">
      <p><strong>아이디:</strong> {{ user.username }}</p>
      <p><strong>이메일:</strong> {{ user.email }}</p>

      <hr>

      <p><strong>이름:</strong> {{ user.name }}</p>
      <p><strong>키:</strong> {{ user.height }} cm</p>
      <p><strong>현재 체중:</strong> {{ user.current_weight }} kg</p>
      <p><strong>목표 체중:</strong> {{ user.target_weight }} kg</p>
      <p><strong>골격근량:</strong> {{ user.muscle_mass }}</p>
      <p><strong>체지방률:</strong> {{ user.body_fat }}</p>
      <p><strong>나이:</strong> {{ user.age }}</p>
      <p><strong>성별:</strong> {{ user.gender }}</p>
      <p><strong>알레르기:</strong> {{ user.allergies }}</p>
    </div>

    <div class="btns">
      <button @click="$router.push('/profile/edit')">프로필 수정</button>
      <button @click="$router.push('/account/edit')">계정 수정</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
const auth = useAuthStore()
const user = auth.user
</script>

<style scoped>
.page {
  width: 330px;
  margin: 30px auto;
}
.box {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 10px;
  background: #fafafa;
}
.btns {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;
}
button {
  padding: 8px;
  cursor: pointer;
}
</style>