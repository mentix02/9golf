<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";
import { fetchCourses } from "@/api/course";
import type { Course } from "@/api/types/course";
import CourseListCard from "@/components/course/CourseListCard.vue";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();
const paginatedCourseResponse = ref<PaginatedResponse<Course>>({
  count: 0,
  next: null,
  results: [],
  previous: null,
});

watch(
  () => authStore.isAuthenticated,
  async (isAuthenticated) => !isAuthenticated && (await router.push({ name: "login" })),
  { immediate: true },
);

onMounted(async () => {
  try {
    paginatedCourseResponse.value = await fetchCourses();
  } catch (err: any) {
    alertStore.error(err.message);
  }
});
</script>

<template>
  <div class="row">
    <div class="col-sm-12 col-md-4" v-for="course of paginatedCourseResponse.results" :key="course.id">
      <CourseListCard :course="course" />
    </div>
  </div>
</template>
