<script setup lang="ts">
const p = defineProps<{
  message: string,
}>()
</script>

<template>
<div class="my-message">
  {{ p.message}}
</div>
</template>

<style scoped>
.my-message {
  border-radius: 6px;
  width: max-content;
  padding: 3px 12px;
  background-color: var(--color-green-light);
  word-wrap: break-word; /* Позволяет переносить длинные слова */
  word-break: break-word; /* Альтернативный способ для переносов */
  overflow-wrap: break-word; /* Поддержка в большинстве современных браузеров */
  max-width: 100%;
}
</style>