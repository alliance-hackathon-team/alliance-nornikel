<script setup lang="ts">
import {Ref, ref, watch} from "vue";
import {getBackendAdapter} from "../../../services/backend/adapters.ts";
import {TargetFile} from "../../../services/backend/domain.ts";
import TargetFileComponent from "./target-file-component.vue";
// import TargetFileComponent from "./target-file-component.vue";

const searchString = ref("")
const targetFiles: Ref<TargetFile[]> = ref([])

watch(searchString, async (val: string) => {
  targetFiles.value = await getBackendAdapter().getTargetFiles(val)
}, {immediate: true})

</script>

<template>
  <div>
    <div class="container">
      <input
          type="search"
          placeholder="Search..."
          v-model.lazy="searchString"
          @keyup.esc="() => searchString = ''"
      >
      <button>
        Search
      </button>
    </div>
    <div>
      {{ searchString }}
    </div>

    <div class="result-container">
      <target-file-component
          v-for="item in targetFiles"
          :target-file="item"
      />
    </div>

  </div>
</template>

<style scoped>
.container {
  display: flex; /* Используем flexbox для распределения пространства */
  justify-content: center; /* Центруем содержимое по горизонтали */
  align-items: center; /* Центруем элементы по вертикали */
  width: 100%;
  max-width: 900px;
  margin: 20px auto;
  box-sizing: border-box; /* Учитываем отступы в ширине */
  padding: 10px;
  gap: 10px; /* Расстояние между элементами */
}

.container input[type="search"] {
  flex: 1; /* Занимает всё оставшееся пространство */
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Учитываем внутренние отступы */
}

.container button {
  flex-shrink: 0; /* Кнопка сохраняет свою ширину и не сжимается */
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.container button:hover {
  background-color: var(--color-primary-hover);
}


.result-container {
  display: flex; /* Используем flexbox для распределения пространства */
  width: 100%;
  max-width: 900px;
  margin: 20px auto;
  box-sizing: border-box; /* Учитываем отступы в ширине */
  padding: 10px;
  gap: 10px; /* Расстояние между элементами */
  flex-wrap: wrap;
}
</style>