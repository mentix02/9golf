import type { User } from "@/api/types/auth";

export type EmbeddedCourse = {
  readonly id: number;
  readonly name: string;
  readonly images: string[];
  readonly is_public: boolean;
};

export interface Session {
  readonly id: number;
  readonly timestamp: string;
  readonly player_count: number;
  readonly course: EmbeddedCourse;
}

export interface SessionWithUsers extends Session {
  users: User[];
}
