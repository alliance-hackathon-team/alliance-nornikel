<script setup lang="ts">
import {ref} from "vue";

const e = defineEmits<{
  (e: "onSearch", searchString: string): void,
}>()

interface P {
  clearAfterInput: boolean,
  btnText: string,
  placeholder?: string,
  waits?: boolean,
}

const p = withDefaults(defineProps<P>(), {
  placeholder: "",
  waits: false,
})


const searchString = ref("")

const handleClickOnEnter = () => {
  if (p.waits) {
    return
  }
  e("onSearch", searchString.value)
  if (p.clearAfterInput) {
    searchString.value = ""
  }
}

const handleClickOnEsc = () => {
  if (p.waits) {
    return
  }
  searchString.value = ""
  e("onSearch", searchString.value)

}

const handleClickOnButton = () => {
  if (p.waits) {
    return
  }
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
        class="search-input  my-height"
    >
    <button
        @click="handleClickOnButton"
        class="btn btn-primary my-height search-button"
    >
      {{ p.waits ? "Жду ответ..." : p.btnText }}
    </button>
  </div>
</template>

<style scoped>

.search-input[type="search"] {
  flex: 1; /* Занимает всё оставшееся пространство */
  padding: 10px;
  font-size: 16px;
  border: 1px solid var(--color-blue-2);
  border-radius: 30px;
  box-sizing: border-box; /* Учитываем внутренние отступы */
}

.search-button {
  flex-shrink: 0; /* Кнопка сохраняет свою ширину и не сжимается */
  width: 120px;
}


.my-height{
  height: 40px;
}
</style>