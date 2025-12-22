<template>
  <DinnerCalendar @select-date="openDinnerModal" />

  <BaseModal v-if="selectedDate" @close="closeModal">
    <DinnerCard
      :date="selectedDate"
      @close="closeModal"
    />
  </BaseModal>
</template>

<script setup>
import { ref } from "vue"

import DinnerCalendar from "@/components/calendar/DinnerCalendar.vue"
import DinnerCard from "@/components/meal/DinnerCard.vue"
import BaseModal from "@/components/common/BaseModal.vue"

const selectedDate = ref(null)

/* 날짜 클릭 */
const openDinnerModal = (dateKey) => {
  console.log("📅 선택된 날짜:", dateKey)
  selectedDate.value = dateKey
}

const closeModal = () => {
  selectedDate.value = null
}
</script>
