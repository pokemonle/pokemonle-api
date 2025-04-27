import axios from "axios";
import qs from "qs";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 1000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  paramsSerializer: (params) => qs.stringify(params, { arrayFormat: "repeat" }),
});

export const fetcher = (url: string, params: unknown = {}) => {
  return instance
    .get(url, {
      params,
    })
    .then((res) => res.data);
};

export default instance;
