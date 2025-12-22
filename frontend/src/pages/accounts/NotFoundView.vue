<template>
  <div class="not-found-container">
    <div class="error-code">404</div>
    <h1>페이지를 찾을 수 없습니다</h1>
    <p>요청하신 주소가 잘못되었거나 삭제된 페이지입니다.</p>
    <router-link to="/community" class="home-button">
      커뮤니티로 돌아가기
    </router-link>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  text-align: center;
  color: #1e293b;
}

.error-code {
  font-size: 8rem;
  font-weight: 900;
  color: #22c55e; /* 기존 테마 컬러 */
  line-height: 1;
  margin-bottom: 20px;
  opacity: 0.2;
}

h1 { font-size: 2rem; margin-bottom: 16px; }
p { color: #64748b; margin-bottom: 40px; }

.home-button {
  padding: 14px 28px;
  background-color: #0f172a;
  color: white;
  border-radius: 14px;
  text-decoration: none;
  font-weight: 800;
  transition: 0.3s;
}

.home-button:hover {
  background-color: #22c55e;
  transform: translateY(-3px);
}
</style>