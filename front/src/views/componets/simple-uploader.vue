<script setup lang="ts">
import {ref, Ref} from "vue";
import {getBackendAdapter} from "../../services/backend/adapters.ts";


// Определяем типы
const fileInput: Ref<HTMLInputElement | null> = ref(null);
const selectedFiles: Ref<File[]> = ref([]);
const uploading: Ref<boolean> = ref(false);
const uploadSuccess: Ref<boolean> = ref(false);
const uploadError: Ref<boolean> = ref(false);

// Открытие диалога выбора файлов
const triggerFileInput = (): void => {
  fileInput.value?.click();
};

// Обработка выбора файлов
const handleFileSelect = (event: Event): void => {
  const input = event.target as HTMLInputElement;
  if (input?.files) {
    const files = Array.from(input.files); // Преобразуем FileList в массив
    selectedFiles.value.push(...files);
  }
  input.value = ""; // Сбрасываем input для повторного выбора тех же файлов
};

// Удаление файла из списка
const removeFile = (index: number): void => {
  selectedFiles.value.splice(index, 1);
};

// Загрузка файлов
const uploadFiles = async (): Promise<void> => {
  uploading.value = true;
  uploadSuccess.value = false;
  uploadError.value = false;

  const formData = new FormData();
  selectedFiles.value.forEach((file) => {
    formData.append("files", file);
  });

  try {
    // Передаём файлы на бэкенд
    await getBackendAdapter().uploadFiles(selectedFiles.value);
    uploadSuccess.value = true;
    selectedFiles.value = []; // Очищаем список после успешной загрузки
  } catch (error) {
    uploadError.value = true;
    console.error("Ошибка загрузки файлов:", error);
  } finally {
    uploading.value = false;
  }
};

</script>

<template>
  <div class="file-uploader">
    <input
        type="file"
        multiple
        ref="fileInput"
        @change="handleFileSelect"
        class="hidden"
    />
    <ul>
      <li
          v-for="(file, index) in selectedFiles"
          :key="index"
          class="mt-6"
      >
        {{ file.name.slice(0, 7) }} ({{ (file.size / 1024).toFixed(2) }} KB)
        <button
            @click="removeFile(index)"
            class="btn btn-outline-primary ml-12"
        >
          Удалить
        </button>
      </li>
    </ul>

    <div class="flex-wrapper flex-direction-column flex-gap-6 mt-12">
      <button
          @click="triggerFileInput"
          class="btn btn-outline-primary"
      >
        Выбрать файлы
      </button>
      <button
          @click="uploadFiles"
          :disabled="!selectedFiles.length || uploading"
          class="btn btn-primary"
      >
        Загрузить
      </button>
    </div>
    <div v-if="uploading">Загрузка...</div>
    <div v-if="uploadSuccess">Файлы успешно загружены!</div>
    <div v-if="uploadError">Ошибка при загрузке файлов!</div>
  </div>
</template>


<style scoped>
.file-uploader {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 300px;
  margin: 0 auto;
  background: white;
}

.hidden {
  display: none;
}


ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
