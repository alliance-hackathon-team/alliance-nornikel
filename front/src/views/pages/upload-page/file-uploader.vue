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

<script>
import { ref } from "vue";
import {getBackendAdapter} from "../../../services/backend/adapters";

export default {
  name: "FileUploader",
  setup() {
    const fileInput = ref(null);
    const selectedFiles = ref([]);
    const uploading = ref(false);
    const uploadSuccess = ref(false);
    const uploadError = ref(false);

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files);
      selectedFiles.value.push(...files);
      event.target.value = ""; // Сброс input для повторного выбора файлов
    };

    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1);
    };

    const uploadFiles = async () => {
      uploading.value = true;
      uploadSuccess.value = false;
      uploadError.value = false;

      const formData = new FormData();
      selectedFiles.value.forEach((file) => {
        formData.append("files", file);
      });

      try {
        await getBackendAdapter().uploadFiles(selectedFiles.value);
        uploadSuccess.value = true;
        selectedFiles.value = []; // Очищаем список после успешной загрузки
      } catch (error) {
        uploadError.value = true;
        console.error(error);
      } finally {
        uploading.value = false;
      }
    };

    return {
      fileInput,
      selectedFiles,
      uploading,
      uploadSuccess,
      uploadError,
      triggerFileInput,
      handleFileSelect,
      removeFile,
      uploadFiles,
    };
  },
};
</script>

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
