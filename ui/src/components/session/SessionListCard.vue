<script lang="ts" setup>
import dayjs from "dayjs";

import type { Session } from "@/api/types/play";
import { extractImageOrPlaceholder } from "@/components/course/utils";

defineProps<{ session: Session }>();
</script>

<template>
  <div class="card mb-3">
    <RouterLink :to="{ name: 'session', params: { id: session.id } }">
      <img :src="extractImageOrPlaceholder(session.course)" class="card-img-top" alt="..." />
    </RouterLink>
    <div class="card-body">
      <h4 class="card-title">{{ session.course.name }}</h4>
      <h6 class="card-subtitle mb-2 text-body-secondary">
        {{ dayjs(session.timestamp).format("MMM DD, YYYY") }}
      </h6>
      <RouterLink :to="{ name: 'session', params: { id: session.id } }" class="btn btn-primary">View</RouterLink>
    </div>
  </div>
</template>
