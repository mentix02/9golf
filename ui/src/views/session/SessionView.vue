<script lang="ts" setup>
import { z } from "zod";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

import useAlertStore from "@/stores/alert";
import { fetchSessionDetails } from "@/api/play";
import type { SessionWithUsers } from "@/api/types/play";

const route = useRoute();
const { id } = route.params;
const alertStore = useAlertStore();

const session = ref<SessionWithUsers>();

watch(
  () => route.params.id,
  async (id) => {
    const positiveIntSchema = z.coerce.number().int().positive();
    const result = await positiveIntSchema.spa(id);

    if (!result.success) {
      alertStore.error("Invalid session ID provided");
      return;
    }

    try {
      session.value = await fetchSessionDetails(result.data);
    } catch (err: any) {
      alertStore.error(err.message);
    }
  },
  { immediate: true }
);
</script>

<template>
  <h1>Session {{ id }}</h1>
  <ol>
    <li v-for="user in session?.users" :key="user.id">
      {{ user.username }}
    </li>
  </ol>
</template>
