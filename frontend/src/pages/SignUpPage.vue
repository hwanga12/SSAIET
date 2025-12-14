<template>
  <div class="page">
    <h1>회원가입</h1>
    <SignupForm />
  </div>
</template>

<script setup>
import SignupForm from "@/components/auth/SignupForm.vue"
</script>

<style scoped>
.page {
  width: 350px;
  margin: 40px auto;
}
</style>