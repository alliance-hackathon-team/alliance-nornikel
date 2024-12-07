<script setup lang="ts">
import {ref} from "vue";

const e = defineEmits<{
  (e: "onSearch", searchString: string): void,
}>()

interface P {
  clearAfterInput: boolean,
  btnText: string,
  placeholder?: string,
}

const p = withDefaults(defineProps<P>(), {
  placeholder: "",
})


const searchString = ref("")

const handleClickOnEnter = () => {
  e("onSearch", searchString.value)
  if (p.clearAfterInput) {
    searchString.value = ""
  }
}

const handleClickOnEsc = () => {
  searchString.value = ""
  e("onSearch", searchString.value)

}

const handleClickOnButton = () => {
  e("onSearch", searchString.value)
  if (p.clearAfterInput) {
    searchString.value = ""
  }
}

</script>

<template>
  <div
      class="flex-wrapper"
      style="width: 100%"
  >
    <input
        type="search"
        :placeholder="p.placeholder"
        v-model.lazy="searchString"
        @keyup.esc="handleClickOnEsc"
        @keyup.enter="handleClickOnEnter"
        class="search-input"
    >
    <button
        @click="handleClickOnButton"
        class="search-button"
    >
      {{ p.btnText }}
    </button>
  </div>
</template>

<style scoped>

.search-input[type="search"] {
  flex: 1; /* Занимает всё оставшееся пространство */
  padding: 10px;
  font-size: 16px;
  border: 1px solid var(--color-blue-2);
  border-radius: 4px;
  box-sizing: border-box; /* Учитываем внутренние отступы */
}

.search-button {
  flex-shrink: 0; /* Кнопка сохраняет свою ширину и не сжимается */
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: var(--color-primary-hover);
}
</style>