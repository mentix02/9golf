import useAuthStore from "@/stores/auth";

export enum AuthResponseCode {
  FAILED,
  SUCCESS,
}

type TokenHeader = {
  Authorization: string;
};

const useTokenHeader = (prefix: string = "Token"): TokenHeader => {
  const { token } = useAuthStore();

  return { Authorization: `${prefix} ${token}` };
};

export default useTokenHeader;
