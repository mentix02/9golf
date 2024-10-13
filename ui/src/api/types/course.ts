export interface Course {
  readonly id: number;

  name: string;
  images: string[];
  added_on: string;
  is_public: boolean;
  description: string;
}

export type Hole = {
  par: number;
  number: number;
  distance: number;
};

export interface CourseWithHoles extends Course {
  readonly holes: Hole[];
}
