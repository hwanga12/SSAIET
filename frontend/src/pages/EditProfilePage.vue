<template>
  <div class="page">
    <h1>프로필 수정</h1>

    <div class="form">
      <label>이름</label>
      <input v-model="profile.name">

      <label>키(cm)</label>
      <input type="number" v-model.number="profile.height">

      <label>현재 체중(kg)</label>
      <input type="number" v-model.number="profile.current_weight">

      <label>목표 체중(kg)</label>
      <input type="number" v-model.number="profile.target_weight">

      <label>골격근량</label>
      <input type="number" v-model.number="profile.muscle_mass">

      <label>체지방률</label>
      <input type="number" v-model.number="profile.body_fat">

      <label>나이</label>
      <input type="number" v-model.number="profile.age">

      <label>성별</label>
      <input v-model="profile.gender">

      <label>알레르기</label>
      <input v-model="profile.allergies">
    </div>

    <button @click="save">저장하기</button>
  </div>
</template>

<script setup>
import { reactive } from "vue"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()

// 🔥 현재 유저 정보 기반으로 초기값 설정
const profile = reactive({ ...auth.user })

const save = async () => {
  await auth.updateProfile(profile)
  alert("프로필이 수정되었습니다!")
}
</script>

<style scoped>
.page { width: 330px; margin: 30px auto; }
.form { display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }
input { padding: 6px; }
button { padding: 8px; cursor: pointer; width: 100%; }
</style>