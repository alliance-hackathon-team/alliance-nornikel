<script setup lang="ts">

import SearchInput from "../componets/search-input.vue";
import {nextTick, ref, Ref} from "vue";
import {LLMResponse} from "../../services/backend/domain.ts";
import {getBackendAdapter} from "../../services/backend/adapters.ts";
import LlmResponse from "../componets/llm-response.vue";
import MyMessage from "../componets/my-message.vue";

type Message = string | LLMResponse

const messages: Ref<Message[]> = ref([])
const loading = ref(false)


const chatContainerRef = ref<HTMLElement | null>(null);
// Функция для прокрутки вниз
const scrollToBottom = () => {
  const chatContainer = chatContainerRef.value;
  if (chatContainer) {
    chatContainer.scrollTo({
      top: chatContainer.scrollHeight,
      behavior: "smooth", // Плавная прокрутка
    });
  }
};

const handleClickOnSearch = async (value: string) => {
  try {
    if (value.length > 0) {
      loading.value = true
      messages.value.push(value)
      const response = await getBackendAdapter().getLLMResponse(value)
      messages.value.push(response)
      await nextTick() // Ждем, пока Vue обновит DOM
      scrollToBottom()
      loading.value = false
    }
  } catch (err) {
    console.error(err)
    messages.value.push("ERROR_" + String(err))
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <div class="flex-wrapper justify-center">

      <div
          class="mt-48 chat-container"
          ref="chatContainerRef"
      >
        <div
            class="mt-24"
            v-for="msg in messages"
        >
          <llm-response
              :llm-response="msg"
              v-if="typeof msg === 'object'"
          />
          <my-message
              :message="msg"
              v-else
          />
        </div>
      </div>

      <div class="search-container">
        <search-input
            @on-search="handleClickOnSearch"
            :clear-after-input="true"
            btn-text="Отправить"
            :waits="loading"
            placeholder="Напишите вопрос, и я отвечу на основе данных Норникеля"
        />
      </div>
  </div>

</template>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 900px;
  height: calc(100vh - 180px);
  background: white;
  padding: 6px 12px;
  border-radius: 6px;
  overflow: auto;
}

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


</style>