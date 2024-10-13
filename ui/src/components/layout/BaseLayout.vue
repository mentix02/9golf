<script lang="ts" setup>
import useAlertStore from "@/stores/alert";
import Alert from "@/components/layout/Alert.vue";
import Navigation from "@/components/layout/Navigation.vue";

const alertStore = useAlertStore();

const handleClose = (index: number) => alertStore.removeAlert(index);
</script>

<template>
  <Navigation />
  <Alert
    class="container"
    :type="alert.type"
    :message="alert.message"
    v-if="alertStore.hasAlerts"
    @close="handleClose(index)"
    v-for="(alert, index) in alertStore.alerts"
  >
    {{ alert.message }}
  </Alert>
  <main class="container">
    <slot />
  </main>
</template>
