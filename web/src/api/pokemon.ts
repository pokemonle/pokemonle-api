import client from "../utils/axios";

export const searchPokemonNames = (url: string) =>
  client.get(url).then((res) => res.data);
