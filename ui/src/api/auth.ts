import configureEndpoint from "@/api/host";

import type { Credentials, TokenResponse } from "./types/auth";

const BASE_URL = configureEndpoint("api/v1/user");

export const fetchTokenResponse = async ({ username, password }: Credentials): Promise<TokenResponse> => {
  let resp: Response;
  const formData = new FormData();

  formData.set("username", username);
  formData.set("password", password);

  try {
    resp = await fetch(`${BASE_URL}/token/`, { method: "POST", body: formData });
  } catch (err: any) {
    throw new Error("Failed to authenticated. Please check your internet connection.");
  }

  if (!resp.ok) {
    throw new Error("Failed to authenticated. Please check your credentials.");
  }

  return await resp.json();
};
