import { ref, toValue } from "vue";
import type { Ref, MaybeRefOrGetter } from "vue";

interface Loader {
  isLoading: Ref<boolean>;
  stopLoading: () => boolean;
  startLoading: () => boolean;
}

export default function useLoader(initial: MaybeRefOrGetter<boolean> = false): Loader {
  const isLoading = ref(toValue(initial));

  const startLoading = () => (isLoading.value = true);

  const stopLoading = () => (isLoading.value = false);

  return { isLoading, startLoading, stopLoading };
}
