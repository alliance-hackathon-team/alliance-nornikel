<script setup lang="ts">
import {TargetFile} from "../../services/backend/domain.ts";

const p = defineProps<{
  targetFile: TargetFile,
  searchString?: string,
}>();

const handleClickOnCard = () => {
  window.open(p.targetFile.src, "_blank");
};

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
      @click="handleClickOnCard"
  >
    <div>
      <!-- Подсвечиваем текст -->
    </div>
    <div class="font-bold">
      <span v-html="highlightText(p.targetFile.title + p.targetFile.extension, searchString)"></span>
    </div>
    <div class="mt-12 multiline-ellipsis">
      <span v-html="highlightText(p.targetFile.content, searchString)"></span>
    </div>
  </div>
</template>

<style scoped>
.target-file {
  border-radius: 6px;
  border: 1px solid var(--color-blue-2);
  padding: 6px 12px;
  width: calc(100% / 2 - 5px);
  height: 300px;
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
</style>
