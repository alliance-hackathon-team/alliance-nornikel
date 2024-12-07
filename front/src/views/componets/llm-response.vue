<script setup lang="ts">
import {LLMResponse} from "../../services/backend/domain.ts";

const p = defineProps<{
  llmResponse: LLMResponse,
}>()
</script>

<template>
  <div class="llm-message">
    <div>
      {{ p.llmResponse.content }}
    </div>
    <div class="mt-6">
      <div>
        Источники:
      </div>
      <div class="">
        <div v-for="source in p.llmResponse.sources">
          <a :href="source.src" target="_blank">
            {{ source.title }}
          </a>
          <span>
            [страницы {{ String(source.pages) }}]
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.llm-message {
  border-radius: 6px;
  width: max-content;
  padding: 3px 12px;
  background-color: var(--color-blue-2);
  word-wrap: break-word; /* Позволяет переносить длинные слова */
  word-break: break-word; /* Альтернативный способ для переносов */
  overflow-wrap: break-word; /* Поддержка в большинстве современных браузеров */
  max-width: 100%;
}
</style>