<script setup lang="ts">
import {handleClickOnLogo, unauthMenuItems} from "./domain.ts";


</script>

<template>
  <div class="horizontal-menu horizontal-menu-top flex-wrapper flex-gap-24 align-center">

    <div
        style="font-weight: bold;"
        @click="handleClickOnLogo"
    >
      Alliance
    </div>

    <div class="flex-wrapper flex-gap-12">
      <div
          class="horizontal-menu-item"
          v-for="item in unauthMenuItems"
          @click="item.onClick"
      >
        {{ item.title }}
      </div>


    </div>

  </div>

</template>

<style scoped>
@import "menu-horizontal.css";
</style>