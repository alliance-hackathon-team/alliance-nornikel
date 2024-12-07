<script setup lang="ts">
import {HorizontalMenu} from "./router/main-menu";
</script>

<template>
  <div style="background: var(--color-blue-0); min-height: 100vh;">
    <horizontal-menu/>
    <router-view style="padding-top: 38px;"/>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  overflow-y: scroll;
}
</style>
