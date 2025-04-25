import client from "../utils/axios";
import useSWR from "swr";

const fetcher = (url: string, params: unknown = {}) => {
  return client
    .get(url, {
      params,
    })
    .then((res) => res.data);
};

export const usePokemonName = (search?: string) =>
  useSWR<PokemonName[]>(["/pokemon/name", search], ([url, search]) =>
    fetcher(url, { search })
  );

export const useGenerations = () => useSWR<GenerationName[]>("/gen", fetcher);
