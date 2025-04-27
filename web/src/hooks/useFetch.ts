import { fetcher } from "../utils/axios";
import useSWR from "swr";

export const usePokemonName = (genIDs: Array<number>, search?: string) =>
  useSWR<PokemonName[]>(
    ["/pokemon/name", search, genIDs],
    ([url, search, gen]) => fetcher(url, { search, gen })
  );

export const usePokemonIDByGeneration = (generations: Array<number>) =>
  useSWR<number[]>(["/pokemon/ids", generations], ([url, gens]) =>
    fetcher(url, { gen: gens })
  );

export const useGenerationList = () =>
  useSWR<GenerationName[]>("/gen", fetcher);
