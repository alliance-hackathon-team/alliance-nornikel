<script setup lang="ts">
import {onMounted, Ref, ref} from "vue";

interface P {
  options?: IntersectionObserverInit,
}

const p = withDefaults(defineProps<P>(), {
  options: () => ({
    rootMargin: "0px 0px 0px 0px",
    threshold: 0,
  }),
})

const e = defineEmits<{
  (e: "intersected"): void,
}>()


function createPaginationObserver(): IntersectionObserver {
  const callback = (entries: IntersectionObserverEntry[], _observer: IntersectionObserver) => {
    const entry = entries[0]
    if (entry.isIntersecting) {
      e("intersected")
    }
  }

  return new IntersectionObserver(callback, p.options)
}

const observer = createPaginationObserver()
const root: Ref<HTMLDivElement | undefined> = ref()

onMounted(() => {
  observer.observe(root.value!)
})
</script>

<template>
  <div
      ref="root"
      class="full-width my-observer"
  >

  </div>
</template>

<style scoped>

</style>