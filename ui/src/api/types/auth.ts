export type TokenResponse = {
  readonly token: string;
  readonly avatar: string;
  readonly username: string;
};

export type Credentials = {
  username: string;
  password: string;
};

export type User = {
  readonly id: number;
  readonly avatar: string;
  readonly username: string;
  readonly last_name: string;
  readonly first_name: string;
};
