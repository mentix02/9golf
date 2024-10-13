<script lang="ts" setup>
import type { Alert } from "@/stores/alert";

defineProps<Alert>();

const emit = defineEmits<{ (e: "close"): void }>();

const handleClose = () => emit("close");
</script>

<template>
  <div class="alert alert-dismissible" :class="`alert-${type}`" role="alert">
    <slot />
    <button @click="handleClose" type="button" class="btn-close" aria-label="Close" />
  </div>
</template>
