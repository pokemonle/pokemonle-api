import request from "@/utils/request";

export const listPokemonName = ({ search } = {}) =>
  request({
    url: "/pokemon/name",
    method: "get",
    params: { search },
  });
