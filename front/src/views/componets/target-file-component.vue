<script setup lang="ts">
import {TargetFile} from "../../services/backend/domain.ts";
import {ref} from "vue";

const p = defineProps<{
  targetFile: TargetFile,
  searchString?: string,
}>();

const showSmallWindow = ref(false)

const handleClickOnCard = async (src: string) => {
  showSmallWindow.value = true
  await navigator.clipboard.writeText(src)
  setTimeout(() => showSmallWindow.value = false, 15_000)
}

// Функция для подсветки совпадений
const highlightText = (text: string, search: string | undefined): string => {
  if (!search || !search.trim()) {
    return text; // Если searchString пустая, возвращаем текст без изменений
  }
  const escapedSearch = search.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escapedSearch})`, "gi");
  // Оборачиваем совпадения в span
  return text.replace(regex, `<span style="background: yellow">$1</span>`)
};
</script>

<template>
  <div
      class="target-file"
      @click="handleClickOnCard(p.targetFile.src)"
  >
    <div>
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

    </div>
    <div class="font-bold">
      <span v-html="highlightText(p.targetFile.title + p.targetFile.extension, searchString)"></span>
    </div>
    <div class="mt-12 multiline-ellipsis">
      Номер страницы: {{ p.targetFile.content }}
    </div>
  </div>
</template>

<style scoped>
.target-file {
  border-radius: 6px;
  border: 1px solid var(--color-blue-2);
  padding: 6px 12px;
  width: calc(100% / 2 - 5px);
  height: max-content;
  background: white;
}

.target-file:hover {
  cursor: pointer;
  background: var(--color-blue-2);
}

/* Многострочное ограничение с многоточием */
.multiline-ellipsis {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-clamp: 9; /* Количество строк */
  -webkit-line-clamp: 9; /* Для Webkit-браузеров */
}

.info-window {
  position: fixed;
  top: 38px;
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
