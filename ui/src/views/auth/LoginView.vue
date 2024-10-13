<script lang="ts" setup>
import { useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";

import useAuthStore from "@/stores/auth";
import useAlertStore from "@/stores/alert";
import useLoader from "@/composables/loader";
import { fetchTokenResponse } from "@/api/auth";
import type { Credentials, TokenResponse } from "@/api/types/auth";

const router = useRouter();
const authStore = useAuthStore();
const alertStore = useAlertStore();
const usernameEl = ref<HTMLInputElement | null>(null);
const { isLoading, stopLoading, startLoading } = useLoader();
const credentials = ref<Credentials>({ username: "", password: "" });

const handleLogin = async () => {
  alertStore.clear();
  startLoading();
  try {
    const tokenResp: TokenResponse = await fetchTokenResponse(credentials.value);
    alertStore.success(`Welcome back, ${tokenResp.username}!`);
    authStore.login(tokenResp);
  } catch (err: any) {
    alertStore.error(err.message);
  } finally {
    stopLoading();
  }
};

/* This is some convoluted shit but somehow... makes sense and works.
 * We just want to make sure the page is changed once the user is logged
 * in via a authStore mutation AND make sure that the /login page is not
 * rendered if an authenticated user walks in. Two birds - one stone.
 */
watch(
  () => authStore.isAuthenticated, // monitor (eagerly so) if user is authenticated.
  async (isAuthenticated) => isAuthenticated && (await router.push({ name: "home" })), // if so, redirect to home.
  { immediate: true } // do it all on mount - regardless of a store mutation.
);

onMounted(() => usernameEl.value?.focus());
</script>

<template>
  <div class="row">
    <div class="col-sm-12 col-md-6 mx-auto">
      <div class="card mt-5">
        <div class="card-header">
          <h3 class="card-title text-center">Welcome back to 9Golf</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleLogin">
            <div class="form-group mb-3">
              <label for="username">Username</label>
              <input type="text" id="username" class="form-control" ref="usernameEl" v-model="credentials.username" />
            </div>
            <div class="form-group mb-3">
              <label for="password">Password</label>
              <input type="password" id="password" class="form-control" v-model="credentials.password" />
            </div>
            <div class="mb-3 d-grid">
              <button :disabled="isLoading" type="submit" class="btn btn-primary btn-lg">
                Login
                <span class="spinner-border" v-if="isLoading" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
