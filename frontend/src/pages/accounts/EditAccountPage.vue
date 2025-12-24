<template>
  <div class="account-page">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <div class="account-container">
      <div class="account-card">
        
        <button class="back-circle-btn" @click="goBack" title="뒤로가기">
          <span class="material-icons">arrow_back</span>
        </button>

        <header class="account-header">
          <div class="header-icon">
            <span class="material-icons">manage_accounts</span>
          </div>
          <h1 class="account-title">계정 <span class="highlight">정보</span> 수정</h1>
          <p class="account-subtitle">보안을 위해 개인 정보를 최신 상태로 유지하세요.</p>
        </header>

        <div class="form-body">
          <div class="field">
            <label>아이디</label>
            <div class="input-wrapper">
              <span class="material-icons input-icon">person</span>
              <input v-model="username" disabled class="custom-input disabled" />
            </div>
            <p class="input-hint">아이디는 변경할 수 없습니다.</p>
          </div>

          <div class="field">
            <label>새 비밀번호</label>
            <div class="input-wrapper">
              <span class="material-icons input-icon">lock</span>
              <input
                type="password"
                v-model="password"
                class="custom-input"
                placeholder="변경하지 않으려면 비워두세요"
              />
            </div>
          </div>
        </div>

        <div class="action-area">
          <button class="save-btn" @click="save">
            <span>수정 내용 저장하기</span>
            <span class="material-icons">done_all</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import BaseNavbar from "@/components/common/BaseNavbar.vue"

const router = useRouter()
const auth = useAuthStore()

const username = ref(auth.user.username)
const password = ref("")

const goBack = () => {
  router.back()
}

const save = async () => {
  try {
    await auth.updateAccount({
      username: username.value,
      password: password.value || undefined,
    })
    alert("계정 정보가 성공적으로 수정되었습니다. 🌱")
    router.push("/profile")
  } catch (err) {
    alert("수정 중 오류가 발생했습니다.")
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.account-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #fcfdfd;
  overflow: hidden;
}

/* 배경 장식 */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.2;
}
.blob-green { width: 500px; height: 500px; background: #22c55e; top: -100px; left: -100px; }
.blob-light { width: 400px; height: 400px; background: #e2e8f0; bottom: -100px; right: -50px; }

/* 카드 컨테이너 */
.account-container {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.account-card {
  width: 100%;
  max-width: 460px;
  background: white;
  border-radius: 32px;
  padding: 50px 40px;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.03);
  position: relative;
}

/* 뒤로가기 버튼 */
.back-circle-btn {
  position: absolute;
  top: 30px;
  left: 30px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #f8fafc;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.back-circle-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
  transform: translateX(-3px);
}

/* 헤더 디자인 */
.account-header {
  text-align: center;
  margin-bottom: 40px;
}

.header-icon {
  width: 56px;
  height: 56px;
  background: #f0fdf4;
  color: #22c55e;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

/* 아이콘 크기 살짝 조정 */
.header-icon .material-icons {
  font-size: 32px;
}

.account-title {
  font-size: 1.8rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -1px;
}

.highlight { color: #22c55e; }

.account-subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 8px;
}

/* 폼 디자인 */
.form-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
  margin-left: 4px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  font-size: 20px;
  color: #94a3b8;
}

.custom-input {
  width: 100%;
  height: 50px;
  padding: 0 16px 0 44px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background: #ffffff;
  font-size: 15px;
  color: #1e293b;
  transition: all 0.2s;
}

.custom-input:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

.custom-input.disabled {
  background: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}

.input-hint {
  font-size: 12px;
  color: #94a3b8;
  margin-left: 4px;
  margin-top: 2px;
}

/* 저장 버튼 (SSAIET 딥 블랙 & 그린) */
.save-btn {
  width: 100%;
  height: 56px;
  margin-top: 40px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.1);
}

.save-btn:hover {
  background: #22c55e;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(34, 197, 94, 0.25);
}

.save-btn:active {
  transform: translateY(0);
}

</style>