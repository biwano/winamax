import config from "@/config" 
import axios from "axios"

export default {
	methods: {
		get(path) {
			return axios.get(`${config.endpoint}${path}`).then((response) => response.data);
		},
    post(path, data) {
      return axios.post(`${config.endpoint}${path}`, data).then((response) => response.data);
    }
	},
	computed: {
      sport_id() {
        return parseInt(this.$route.params.sport_id);
      },
      tournament_id() {
        return parseInt(this.$route.params.tournament_id);
      },
      category_id() {
        return parseInt(this.$route.params.category_id);
      },
      match_id() {
        return parseInt(this.$route.params.match_id);
      },
    }
  }
