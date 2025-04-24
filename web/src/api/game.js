import request from "@/utils/request";

export const GameInit = (params) =>
  request({
    url: "/game/init",
    method: "get",
    params,
  });

export const GameGuess = (params) =>
  request({
    url: "/game/guess",
    method: "get",
    params,
  });

export const GameAnswer = (params) =>
  request({
    url: "/game/answer",
    method: "get",
    params,
  });
