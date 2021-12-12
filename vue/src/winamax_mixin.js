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
      route_sport_id() {
        return parseInt(this.$route.params.sport_id);
      },
      route_tournament_id() {
        return parseInt(this.$route.params.tournament_id);
      },
      route_category_id() {
        return parseInt(this.$route.params.category_id);
      },
      route_match_id() {
        return parseInt(this.$route.params.match_id);
      },
    }
  }
