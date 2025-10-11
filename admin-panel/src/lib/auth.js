import axiosInstance from "./axiosInstance";

export const login = async (username, password) => {
  const res = await axiosInstance.post("user/", { username, password });
  return res.data;
};

export const logout = async () => {
  const res = await axiosInstance.post("user/", { action: "logout" });
  return res.data;
};

export const getProfile = async () => {
  const res = await axiosInstance.get("user/");
  return res.data;
};

export const refreshToken = async () => {
  const res = await axiosInstance.get("user/?action=refresh");
  return res.data;
};
