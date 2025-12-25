<template>
  <button class="base-btn">
    <slot />
  </button>
</template>

<style scoped>
.base-btn {
  width: 100%;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.2px;

  color: #ffffff;
  background: linear-gradient(
    135deg,
    #2e7d32,
    #66bb6a
  );

  border: none;
  border-radius: 10px;

  cursor: pointer;
  transition: all 0.2s ease;
}

/* hover */
.base-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
}

/* active */
.base-btn:active {
  transform: translateY(0);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

/* disabled (나중에 쓰기 좋음) */
.base-btn:disabled {
  background: #c8e6c9;
  color: #ffffff;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
