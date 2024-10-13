import { createRouter, createWebHistory } from "vue-router";

import useAuthStore from "@/stores/auth";
import HomeView from "@/views/HomeView.vue";
import CourseView from "@/views/CourseView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";

const router = createRouter({
  linkActiveClass: "active",
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/course/:id",
      name: "course",
      component: CourseView,
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("@/views/auth/ProfileView.vue"),
    },
    {
      path: "/sessions",
      name: "sessions",
      component: () => import("@/views/session/SessionListView.vue"),
    },
    {
      path: "/session/:id",
      children: [
        {
          path: "",
          name: "session",
          component: () => import("@/views/session/SessionView.vue"),
        },
        {
          path: "/session/:id/settings",
          name: "session-settings",
          component: () => import("@/views/session/SessionSettingsView.vue"),
        },
      ],
    },
  ],
});

router.beforeEach((to, from) => {
  const authStore = useAuthStore();
  if (to.name !== "login" && to.name !== "register" && to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" };
  }
  return true;
});

export default router;
