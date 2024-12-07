<script setup lang="ts">
import {Ref, ref, watch} from "vue";
import {getBackendAdapter} from "../../../services/backend/adapters.ts";
import {TargetFile} from "../../../services/backend/domain.ts";
import TargetFileComponent from "../../componets/target-file-component.vue";

const searchString = ref("")
const targetFiles: Ref<TargetFile[]> = ref([])

const handleSearch = async () => targetFiles.value = await getBackendAdapter().getTargetFiles(searchString.value)
watch(searchString, handleSearch, {immediate: true})

</script>

<template>
  <div>
    <div class="search-container bg-blue-0">
      <input
          type="search"
          placeholder="Search..."
          v-model.lazy="searchString"
          @keyup.esc="() => searchString = ''"
      >
      <button @click="handleSearch">
        Search
      </button>
    </div>

    <div class="result-container">
      <target-file-component
          v-for="item in targetFiles"
          :target-file="item"
          :search-string="searchString"
      />
    </div>

  </div>
</template>

<style scoped>
.search-container {
  position: sticky;
  top: 38px;
  display: flex; /* Используем flexbox для распределения пространства */
  justify-content: center; /* Центруем содержимое по горизонтали */
  align-items: center; /* Центруем элементы по вертикали */
  width: 100%;
  max-width: 900px;
  margin: 24px auto;
  box-sizing: border-box; /* Учитываем отступы в ширине */
  gap: 10px; /* Расстояние между элементами */
}

.search-container input[type="search"] {
  flex: 1; /* Занимает всё оставшееся пространство */
  padding: 10px;
  font-size: 16px;
  border: 1px solid var(--color-blue-2);
  border-radius: 4px;
  box-sizing: border-box; /* Учитываем внутренние отступы */
}

.search-container button {
  flex-shrink: 0; /* Кнопка сохраняет свою ширину и не сжимается */
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.search-container button:hover {
  background-color: var(--color-primary-hover);
}


.result-container {
  display: flex; /* Используем flexbox для распределения пространства */
  width: 100%;
  max-width: 900px;
  margin: 20px auto;
  box-sizing: border-box; /* Учитываем отступы в ширине */
  gap: 10px; /* Расстояние между элементами */
  flex-wrap: wrap;
}
</style>