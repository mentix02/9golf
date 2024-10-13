<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

import BaseLayout from "@/components/layout/BaseLayout.vue";

export default defineComponent({
  name: "9Golf",
  components: { RouterView, BaseLayout },
});
</script>

<template>
  <BaseLayout>
    <RouterView />
  </BaseLayout>
</template>
