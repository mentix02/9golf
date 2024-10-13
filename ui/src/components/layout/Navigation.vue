<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import useAuthStore from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const isOpen = ref<boolean>(false);

const toggleNavigation = () => (isOpen.value = !isOpen.value);

const logout = () => {
  authStore.logout();
  toggleNavigation();
  router.push({ name: "home" });
};
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-primary mb-4" data-bs-theme="dark">
    <div class="container">
      <RouterLink class="navbar-brand" :to="{ name: 'home' }">9Golf</RouterLink>
      <button
        type="button"
        class="navbar-toggler"
        @click="toggleNavigation"
        aria-label="Toggle navigation"
        :aria-expanded="isOpen ? 'true' : 'false'"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div :class="{ show: isOpen }" class="collapse navbar-collapse justify-content-end">
        <ul class="navbar-nav" v-if="!authStore.isAuthenticated">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'home' }"> Home </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'login' }"> Login </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'register' }"> Register </RouterLink>
          </li>
        </ul>
        <ul class="navbar-nav" v-else>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'home' }"> Home </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'sessions' }"> Sessions </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'profile' }"> Profile </RouterLink>
          </li>
          <li class="nav-item">
            <a @click="logout" class="nav-link clicker"> Logout </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.clicker {
  cursor: pointer;
}
</style>
