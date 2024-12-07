<script setup lang="ts">
import SimpleUploader from "../componets/simple-uploader.vue";
import SearchInput from "../componets/search-input.vue";
import TargetFileComponent from "../componets/target-file-component.vue";
import {Ref, ref} from "vue";
import {TargetFile} from "../../services/backend/domain.ts";
import {getBackendAdapter} from "../../services/backend/adapters.ts";
import IntersectionObserver from "../componets/intersection-observer.vue";

const searchString = ref("")
const targetFiles: Ref<TargetFile[]> = ref([])
const loading = ref(false)

const handleSearch = async (value: string) => {
  if (loading.value || value.length === 0) {
    return
  }
  try {
    loading.value = true
    searchString.value = value
    targetFiles.value = await getBackendAdapter().getTargetFiles(searchString.value)
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const step = 10
const elementCounter = ref(step)
const increaseMaxElements = () => {
  console.log("intersected")
  elementCounter.value += step
}
</script>

<template>
  <div class="double-page-wrapper">
    <div class="double-page-content mt-48">
      <search-input
          btn-text="Поиск"
          :clear-after-input="false"
          :waits="loading"
          placeholder="Введите название файла, чтобы я его нашел"
          @on-search="handleSearch"
          class="sticky"
      />
      <div class="result-container mt-24">
        <target-file-component
            v-for="item in targetFiles.slice(0, elementCounter)"
            :target-file="item"
            :search-string="searchString"
        />
        <intersection-observer
            @intersected="increaseMaxElements"
        />
      </div>
    </div>
    <div class="double-page-right mt-48">
      <simple-uploader/>


    </div>
  </div>
</template>

<style scoped>
.result-container {
  display: flex; /* Используем flexbox для распределения пространства */
  width: 100%;
  max-width: 900px;
  margin: 20px auto;
  box-sizing: border-box; /* Учитываем отступы в ширине */
  gap: 10px; /* Расстояние между элементами */
  flex-wrap: wrap;
}

.sticky {
  position: sticky;
  top: 38px;
}
</style>