<template>
  <div class="input-group">
    <label class="input-label">{{ label }}</label>

    <input
      class="input-field"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  type: { type: String, default: "text" },
})

defineEmits(["update:modelValue"])
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* 라벨 */
.input-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151; /* gray-700 */
}

/* 입력창 */
.input-field {
  height: 44px;
  padding: 0 12px;

  font-size: 14px;
  color: #111827;

  border-radius: 10px;
  border: 1.5px solid #d1d5db; /* gray-300 */

  background: #ffffff;
  transition: all 0.15s ease;
}

/* 포커스 */
.input-field:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.15);
}

/* placeholder */
.input-field::placeholder {
  color: #9ca3af;
}
</style>