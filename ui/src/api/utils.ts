const signOutAndRedirect = () => {
  localStorage.clear();
  window.location.href = "/login";
};

export const checkAuthFailedOrSignOut = (resp: Response) => {
  if (!resp.ok) {
    switch (resp.status) {
      case 401:
        signOutAndRedirect();
        return;
      case 403:
        signOutAndRedirect();
        return;
      default:
        console.error("Failed to fetch data.");
    }
  }
};
