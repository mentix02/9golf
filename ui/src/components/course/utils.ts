import { z } from "zod";

import type { Course } from "@/api/types/course";
import type { EmbeddedCourse } from "@/api/types/play";

const placeholderUrl = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg";

// Don't try to be clever with these one liners, it's not worth it.
// Except when I do it, then it's fine. Simply extract the image or return a placeholder.
export const extractImageOrPlaceholder = (course?: Course | EmbeddedCourse): string =>
  course ? (course.images.length > 0 ? course.images[0] : placeholderUrl) : placeholderUrl;

export const convertToMetres = (distance_in_yards: number | string): number => {
  const result = z.number().positive().safeParse(distance_in_yards);
  if (result.success) return Math.round(result.data * 0.9144);
  return NaN;
};
