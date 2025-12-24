<template>
  <div class="write-layout">
    <BaseNavbar />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <main class="write-container">
      <header class="write-header">
        <h2 class="page-title">새 이야기 <span class="highlight">작성</span></h2>
        <p class="page-subtitle">SSAFY 동료들과 나누고 싶은 소중한 정보를 들려주세요.</p>
      </header>

      <div class="write-card">
        <div class="field-group">
          <label class="label">카테고리</label>
          <div class="select-wrapper">
            <select v-model="category" class="custom-select">
              <option value="RESTAURANT">🍽️ 식당 추천</option>
              <option value="REVIEW">📈 변화 후기</option>
              <option value="QNA">❓ Q&A</option>
              <option value="FREE">💬 잡담</option>
            </select>
          </div>
        </div>

        <div class="field-group">
          <label class="label">제목</label>
          <input 
            v-model="title" 
            placeholder="제목을 입력하세요" 
            class="custom-input"
          />
        </div>

        <div class="field-group">
          <label class="label">내용</label>
          <textarea 
            v-model="content" 
            placeholder="동료들에게 도움이 될 상세한 내용을 적어주세요." 
            class="custom-textarea"
          ></textarea>
        </div>

        <Transition name="slide-fade">
          <div v-if="category === 'RESTAURANT'" class="extra-info-card restaurant">
            <h4 class="extra-title"><span class="material-icons">storefront</span> 식당 정보 상세</h4>
            <div class="extra-grid">
              <input v-model="restaurant.restaurant_name" placeholder="식당 이름" class="custom-input" />
              <input v-model="restaurant.location" placeholder="위치 (예: 역삼역 3번출구)" class="custom-input" />
              <input v-model="restaurant.recommended_menu" placeholder="추천 메뉴" class="custom-input" />
              <div class="select-wrapper">
                <select v-model="restaurant.health_tag" class="custom-select">
                  <option value="BALANCED">🥗 균형식</option>
                  <option value="HIGH_PROTEIN">🥩 고단백</option>
                  <option value="LOW_FAT">🥑 저지방</option>
                  <option value="DIET">📉 다이어트</option>
                  <option value="OUT">🍜 외식 (치팅)</option>
                </select>
              </div>
            </div>
          </div>

          <div v-else-if="category === 'REVIEW'" class="extra-info-card review">
            <h4 class="extra-title"><span class="material-icons">monitor_weight</span> 체중 변화 기록</h4>
            <div class="extra-grid">
              <div class="field-group-inner">
                <label class="sub-label">진행 기간</label>
                <div class="select-wrapper">
                  <select v-model="review.period" class="custom-select">
                    <option value="1W">1주일 진행</option>
                    <option value="2W">2주일 진행</option>
                    <option value="1M">1개월 진행</option>
                    </select>
                </div>
              </div>
              
              <div class="field-group-inner">
                <label class="sub-label">체중 변화량</label>
                <div class="weight-input-group">
                  <input
                    type="number"
                    v-model="review.weight_diff"
                    placeholder="예: -2.5"
                    class="custom-input no-spinner"
                  />
                  <span class="unit-text">kg</span>
                </div>
              </div>
            </div>
            <p class="input-hint">* 변화량만 입력해주세요 (예: 감량시 -2, 증량시 2)</p>
          </div>
        </Transition>

        <div class="actions">
          <button class="btn-cancel" @click="router.back()">취소</button>
          <button class="btn-submit" @click="submit">
            <span>등록하기</span>
            <span class="material-icons">send</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useCommunityStore } from "@/stores/community"
import BaseNavbar from "@/components/common/BaseNavbar.vue"

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()

const category = ref(route.query.category || "RESTAURANT")
const title = ref("")
const content = ref("")

const restaurant = ref({
  restaurant_name: "",
  location: "",
  recommended_menu: "",
  health_tag: "BALANCED",
})

const review = ref({
  period: "1W",
  change_type: "WEIGHT",
  weight_diff: null,
})

const submit = async () => {
  console.log("🚀 1. 등록 프로세스 시작")
  
  if (!title.value || !content.value) {
    alert("제목과 내용을 입력해주세요!")
    return
  }
  
  try {
    const payload = {
      category: category.value,
      title: title.value,
      content: content.value,
    }
    
    if (category.value === "RESTAURANT") {
      payload.restaurant_info = restaurant.value
    }

    if (category.value === "REVIEW") {
      if (!review.value.weight_diff) {
        alert("체중 변화량을 입력해주세요.")
        return
      }
      payload.review_info = review.value
    }

    console.log("📦 2. 전송 데이터 확인:", payload)
    
    if (typeof store.addPost !== 'function') {
      alert("시스템 오류: 등록 함수를 찾을 수 없습니다.")
      return
    }

    await store.addPost(payload)
    
    router.push(`/community/${category.value.toLowerCase()}`)
    
  } catch (err) {
    const errorMsg = err.response?.data?.detail || "글 작성 중 오류가 발생했습니다."
    alert(errorMsg)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.write-layout {
  min-height: 100vh;
  background-color: #fcfdfd;
  position: relative;
}

/* ================= BACKGROUND ================= */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.15;
}

.blob-green {
  width: 500px;
  height: 500px;
  background: #22c55e;
  top: -100px;
  left: -100px;
}

.blob-light {
  width: 400px;
  height: 400px;
  background: #e2e8f0;
  bottom: -50px;
  right: -50px;
}

/* ================= PAGE ================= */
.write-container {
  position: relative;
  z-index: 1;
  max-width: 750px;
  min-width: 750px;
  margin: 0 auto;
  padding: 120px 20px 100px;
}

/* ================= HEADER ================= */
.write-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 12px;
}

.highlight {
  color: #22c55e;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
}

/* ================= CARD ================= */
.write-card {
  background: white;
  border-radius: 32px;
  padding: 40px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
  margin-left: 4px;
}

/* ================= INPUT ================= */
.custom-input,
.custom-select,
.custom-textarea {
  width: 100%;
  height: 52px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background: #ffffff;
  font-size: 1rem;
  transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
}

.custom-textarea {
  height: 180px;
  padding: 16px;
  resize: none;
  line-height: 1.6;
}

.custom-input:focus,
.custom-select:focus,
.custom-textarea:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

/* ✅ 화살표(Spinner) 제거 스타일 */
.custom-input.no-spinner::-webkit-outer-spin-button,
.custom-input.no-spinner::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.custom-input.no-spinner {
  -moz-appearance: textfield;
}

/* ================= EXTRA INFO ================= */
.extra-info-card {
  background: #f8fafc;
  border-radius: 20px;
  padding: 24px;
  border: 1px dashed #cbd5e1;
}

.extra-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
}

.extra-title .material-icons {
  color: #22c55e;
}

.extra-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.field-group-inner {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #64748b;
  margin-left: 2px;
}

.weight-input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.unit-text {
  position: absolute;
  right: 16px;
  font-weight: 700;
  color: #94a3b8;
}

.input-hint {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 12px;
  text-align: right;
}

/* ================= ACTIONS ================= */
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 20px;
}

button {
  height: 56px;
  border-radius: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.3s;
  border: none;
}

.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
  padding: 0 30px;
}

.btn-cancel:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-submit {
  background: #0f172a;
  color: white;
  padding: 0 40px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.1);
}

.btn-submit:hover {
  background: #22c55e;
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(34, 197, 94, 0.25);
}

/* ================= TRANSITION ================= */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
</style>