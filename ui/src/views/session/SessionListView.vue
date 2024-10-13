<script lang="ts" setup>
import { ref, onMounted } from "vue";

import useAlertStore from "@/stores/alert";
import { fetchSessions } from "@/api/play";
import type { Session } from "@/api/types/play";
import SessionListCard from "@/components/session/SessionListCard.vue";

const alertStore = useAlertStore();
const paginatedSessionsResponse = ref<PaginatedResponse<Session>>({
  count: 0,
  next: null,
  results: [],
  previous: null,
});

onMounted(async () => {
  try {
    paginatedSessionsResponse.value = await fetchSessions();
  } catch (err: any) {
    alertStore.error(err.message);
  }
});
</script>

<template>
  <div class="row">
    <div class="col-sm-12 col-md-4" v-for="session of paginatedSessionsResponse.results" :key="session.id">
      <SessionListCard :session="session" />
    </div>
  </div>
</template>
