<script setup lang="ts">


import {TargetFile} from "../../../services/backend/domain.ts";

const p = defineProps<{
  targetFile: TargetFile,
  searchString?: string,
}>()

const handleClickOnCard = () => {
  window.open(p.targetFile.src, "_blank");
};
</script>

<template>
  <div
      class="target-file"
      @click="handleClickOnCard"
  >
    <div>

    </div>
    <div class="font-bold">
      {{ p.targetFile.title }}{{p.targetFile.extension}}
    </div>
    <div class="mt-12">
      {{p.targetFile.content}}
    </div>
  </div>
</template>

<style scoped>
.target-file {
  border-radius: 6px;
  padding: 6px 12px;
  width: 286px;
  height: 300px;
  background: white;
}

.target-file:hover {
  cursor: pointer;
}
</style>