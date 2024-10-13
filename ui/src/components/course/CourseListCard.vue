<script lang="ts" setup>
import dayjs from "dayjs";

import type { Course } from "@/api/types/course";
import { extractImageOrPlaceholder } from "@/components/course/utils";

defineProps<{ course: Course }>();
</script>

<template>
  <div class="card mb-3">
    <RouterLink :to="{ name: 'course', params: { id: course.id } }">
      <img :src="extractImageOrPlaceholder(course)" class="card-img-top" alt="..." />
    </RouterLink>
    <div class="card-body">
      <h4 class="card-title">{{ course.name }}</h4>
      <h6 class="card-subtitle mb-2 text-body-secondary">{{ dayjs(course.added_on).format("MMM DD, YYYY") }}</h6>
      <RouterLink :to="{ name: 'course', params: { id: course.id } }" class="btn btn-primary">View</RouterLink>
    </div>
  </div>
</template>
