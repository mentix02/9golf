import { defineStore, acceptHMRUpdate } from "pinia";

import useAlertStore from "@/stores/alert";
import type { TokenResponse } from "@/api/types/auth";

export type AuthState = {
  token?: string;
  avatar?: string;
  username?: string;
};

const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({ token: undefined, username: undefined, avatar: undefined }),

  getters: {
    isAuthenticated(): boolean {
      return !!this.token;
    },
  },

  actions: {
    logout() {
      const alertStore = useAlertStore();
      alertStore.clear();
      this.$reset();
    },

    login(tokenResponse: TokenResponse) {
      this.token = tokenResponse.token;
      this.avatar = tokenResponse.avatar;
      this.username = tokenResponse.username;
    },
  },
  persist: true,
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}

export default useAuthStore;
