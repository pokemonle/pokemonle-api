import request from "@/utils/request";

export const getGen = () =>
  request({
    url: "/gen",
    method: "get",
  });
