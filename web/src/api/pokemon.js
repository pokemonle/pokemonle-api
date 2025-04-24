import request from "@/utils/request";

export const listPokemonName = ({ search }) =>
  request({
    url: "/api/pokemon/name",
    method: "get",
    params: { search },
  });
