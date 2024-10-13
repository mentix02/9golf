import useTokenHeader from "@/api/headers";
import configureEndpoint from "@/api/host";
import { checkAuthFailedOrSignOut } from "@/api/utils";
import type { Session, SessionWithUsers } from "@/api/types/play";

const BASE_URL = configureEndpoint("api/v1/score");

export const createSession = async (course_id: number): Promise<Session> => {
  let resp: Response;
  const formData = new FormData();

  formData.set("course", String(course_id));

  try {
    resp = await fetch(`${BASE_URL}/sessions/`, { method: "POST", headers: useTokenHeader() });
  } catch (err: any) {
    throw new Error("Failed to create session. Please check your internet connection.");
  }

  checkAuthFailedOrSignOut(resp);

  if (!resp.ok) throw new Error("Failed to create session.");

  return await resp.json();
};

export const fetchSessions = async (page: number = 1): Promise<PaginatedResponse<Session>> => {
  let resp: Response;

  try {
    resp = await fetch(`${BASE_URL}/sessions/?page=${page}`, { headers: useTokenHeader() });
  } catch (err: any) {
    throw new Error("Failed to fetch sessions. Please check your internet connection.");
  }

  checkAuthFailedOrSignOut(resp);

  if (!resp.ok) throw new Error("Failed to fetch sessions.");

  return await resp.json();
};

export const fetchSessionDetails = async (session_id: number): Promise<SessionWithUsers> => {
  let resp: Response;

  try {
    resp = await fetch(`${BASE_URL}/sessions/${session_id}/`, { headers: useTokenHeader() });
  } catch (err: any) {
    throw new Error("Failed to fetch session details. Please check your internet connection.");
  }

  checkAuthFailedOrSignOut(resp);

  if (!resp.ok) throw new Error("Failed to fetch session details.");

  return await resp.json();
};
