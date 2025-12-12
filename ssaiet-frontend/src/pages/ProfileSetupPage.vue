<template>
  <div class="page">
    <h1>인적사항 입력</h1>
    <ProfileForm />
  </div>
</template>

<script setup>
import ProfileForm from "@/components/auth/ProfileForm.vue"
</script>

<style scoped>
.page {
  width: 350px;
  margin: 40px auto;
}
</style>