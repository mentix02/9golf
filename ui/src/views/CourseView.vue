<script lang="ts" setup>
import { z } from "zod";
import { useRoute } from "vue-router";
import { ref, watch, computed } from "vue";

import useAlertStore from "@/stores/alert";
import { fetchCourseDetails } from "@/api/course";
import type { CourseWithHoles } from "@/api/types/course";
import { convertToMetres, extractImageOrPlaceholder } from "@/components/course/utils";

const route = useRoute();
const alertStore = useAlertStore();
const positiveIntSchema = z.coerce.number().int().positive();

const showInMeters = ref(false);
const course = ref<CourseWithHoles>();
const totalPars = computed<number>(() =>
  course.value ? course.value.holes.reduce((acc, hole) => acc + hole.par, 0) : 0,
);

watch(
  () => route.params.id,
  async (id) => {
    const result = await positiveIntSchema.spa(id);

    if (!result.success) {
      alertStore.error("Invalid course ID provided");
      return;
    }

    try {
      course.value = await fetchCourseDetails(result.data);
    } catch (err: any) {
      alertStore.error(err.message);
    }
  },
  { immediate: true },
);
</script>

<template>
  <div class="row">
    <div class="col-sm-12 col-lg-4">
      <h1>{{ course?.name }}</h1>
      <img :src="extractImageOrPlaceholder(course)" alt="Course Image" class="img-fluid mb-3" />
      <div class="btn-group">
        <button class="btn btn-success">Play</button>
        <button class="btn btn-primary">Bookmark</button>
        <button class="btn btn-secondary">Stats</button>
      </div>
      <hr />
      <p class="newline-text">{{ course?.description }}</p>
      <div class="form-check form-switch">
        <input class="form-check-input" type="checkbox" role="switch" v-model="showInMeters" id="useMeters" />
        <label class="form-check-label" for="useMeters">Use metres</label>
      </div>
    </div>
    <div class="col-sm-12 col-lg-8">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Number</th>
            <th scope="col">Par</th>
            <th scope="col">Distance</th>
            <th scope="col">Units</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hole in course?.holes" :key="hole.number">
            <td>{{ hole.number }}</td>
            <td>{{ hole.par }}</td>
            <td>{{ showInMeters ? convertToMetres(hole.distance) : hole.distance }}</td>
            <td>{{ showInMeters ? "m" : "yards" }}</td>
          </tr>
          <tr>
            <td><strong>Total</strong></td>
            <td>{{ totalPars }}</td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.newline-text {
  white-space: pre-line;
}
</style>
