/// <reference types="vite/client" />

declare type PaginatedResponse<T> = {
  readonly results: T[];
  readonly count: number;
  readonly next: string | null;
  readonly previous: string | null;
};

declare const EmptyPaginatedResponse: PaginatedResponse<never>;
