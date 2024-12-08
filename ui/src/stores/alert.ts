import { acceptHMRUpdate, defineStore } from "pinia";

type AlertType =
  | "primary"
  | "secondary"
  | "success"
  | "danger"
  | "warning"
  | "info"
  | "light"
  | "dark";

export type Alert = {
  readonly type: AlertType;
  readonly message: string;
};

export type AlertState = {
  alerts: Alert[];
};

const useAlertStore = defineStore("alert", {
  state: (): AlertState => ({ alerts: [] }),
  getters: {
    hasAlerts(): boolean {
      return this.alerts.length > 0;
    },
  },
  actions: {
    clear() {
      this.alerts = [];
    },
    addAlert(alert: Alert) {
      this.alerts.push(alert);
    },
    removeAlert(index: number) {
      this.alerts.splice(index, 1);
    },

    // convenience methods
    success(message: string) {
      this.addAlert({ type: "success", message });
    },
    error(message: string) {
      this.addAlert({ type: "danger", message });
    },
    warning(message: string) {
      this.addAlert({ type: "warning", message });
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAlertStore, import.meta.hot));
}

export default useAlertStore;
