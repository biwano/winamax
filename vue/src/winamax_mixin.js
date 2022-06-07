import config from "@/config";
import axios from "axios";

export default {
  methods: {
    get(path) {
      return axios
        .get(`${config.endpoint}${path}`)
        .then((response) => response.data);
    },
    post(path, data) {
      return axios
        .post(`${config.endpoint}${path}`, data)
        .then((response) => response.data);
    },
    date(timestamp) {
      var date = new Date(timestamp * 1000);
      var date_format_str =
        date.getFullYear().toString() +
        "-" +
        ((date.getMonth() + 1).toString().length == 2
          ? (date.getMonth() + 1).toString()
          : "0" + (date.getMonth() + 1).toString()) +
        "-" +
        (date.getDate().toString().length == 2
          ? date.getDate().toString()
          : "0" + date.getDate().toString()) +
        " " +
        (date.getHours().toString().length == 2
          ? date.getHours().toString()
          : "0" + date.getHours().toString()) +
        ":" +
        ((parseInt(date.getMinutes() / 5) * 5).toString().length == 2
          ? (parseInt(date.getMinutes() / 5) * 5).toString()
          : "0" + (parseInt(date.getMinutes() / 5) * 5).toString());
      return date_format_str;
    },
  },
};
