<script setup lang="ts">
import {LLMResponse} from "../../services/backend/domain.ts";
import {ref} from "vue";

const p = defineProps<{
  llmResponse: LLMResponse,
}>()

const showSmallWindow = ref(false)

const openWindow = async (src: string) => {
  showSmallWindow.value = true
  await navigator.clipboard.writeText(src)
  setTimeout(() => showSmallWindow.value = false, 15_000)
}
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
      <div class="" style="position: relative;">
        <div class="info-window" v-if="showSmallWindow">
          <div class="flex-wrapper">
            <div class="font-bold fs-4">
              Вы скопировали ссылку в буфер обмена!
            </div>
            <div class="mt-12">
              Пожалуйста, откройте новую вкладу и вставьте ее в поисковую строку.
              Мы не можем сделать это за вас, так как браузер не любит получать файлы с локального диска (а в рамках хакатона
              мы получаем их именно оттуда). Извините за неудобства.
            </div>
            <div
                @click="() => showSmallWindow = false"
                class="ml-12 cursor-pointer link-style"
            >
              Закрыть
            </div>
          </div>

        </div>

        <div v-for="source in p.llmResponse.sources">
          <a :href="source.src" target="_blank" @click.prevent="openWindow(source.src)">
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


.info-window {
  position: absolute;
  top: -150px;
  left: 0;
  background: var(--color-green-light);
  padding: 3px 6px;
  border-radius: 6px;
}

.link-style {
  color: blue; /* Синий цвет, как у ссылки */
  text-decoration: underline; /* Подчеркивание */
}

.link-style:hover {
  color: darkblue; /* Более темный оттенок синего при наведении */
  text-decoration: underline; /* Сохраняем подчеркивание */
}
</style>