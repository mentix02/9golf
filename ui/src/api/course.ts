import useTokenHeader from "@/api/headers";
import configureEndpoint from "@/api/host";
import { checkAuthFailedOrSignOut } from "@/api/utils";
import type { Course, CourseWithHoles } from "@/api/types/course";

const BASE_URL = configureEndpoint("api/v1/course");

export const fetchCourses = async (page: number = 1): Promise<PaginatedResponse<Course>> => {
  let resp: Response;

  try {
    resp = await fetch(`${BASE_URL}/?page=${page}`, {
      headers: useTokenHeader(),
    });
  } catch (err: any) {
    throw new Error("Failed to fetch courses. Please check your internet connection.");
  }

  checkAuthFailedOrSignOut(resp);

  if (!resp.ok) throw new Error("Failed to fetch courses.");

  return await resp.json();
};

export const fetchCourseDetails = async (course_id: number): Promise<CourseWithHoles> => {
  let resp: Response;

  try {
    resp = await fetch(`${BASE_URL}/${course_id}/`, { headers: useTokenHeader() });
  } catch (err: any) {
    throw new Error("Failed to fetch course details. Please check your internet connection.");
  }

  checkAuthFailedOrSignOut(resp);

  if (!resp.ok) throw new Error("Failed to fetch course details.");

  return await resp.json();
};
