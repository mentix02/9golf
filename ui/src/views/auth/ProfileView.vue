<script lang="ts" setup>
import { watch } from "vue";
import { useRouter } from "vue-router";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();

watch(
  () => authStore.isAuthenticated,
  async (isAuthenticated) => {
    if (!isAuthenticated) {
      alertStore.error("You need to be logged in to view this page.");
      await router.push({ name: "login" });
    }
  },
  { immediate: true }
);
</script>

<template>
  <h1>{{ authStore.username }}'s profile</h1>
</template>
