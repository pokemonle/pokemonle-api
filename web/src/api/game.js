import request from "@/utils/request";

export const initGame = (params) =>
  request({
    url: "/game/init",
    method: "get",
    params,
  });
