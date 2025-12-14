<template>
  <button class="base-btn">
    <slot></slot>
  </button>
</template>

<style scoped>
.base-btn {
  padding: 8px 12px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>