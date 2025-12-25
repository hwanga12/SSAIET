import axios from "axios"

export const predictWeightChange = async () => {
  const res = await axios.post("/meal/predict-weight/");
  return res.data.predicted_weight_change;
};
