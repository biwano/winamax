import config from "@/config" 
import axios from "axios"

export default {
	methods: {
		get(path) {
			return axios.get(`${config.endpoint}${path}`).then((response) => response.data);
		}
	},
	computed: {
      sport_id() {
        return parseInt(this.$route.params.sport_id);
      },
      tournament_id() {
        return parseInt(this.$route.params.tournament_id);
      },
      categorty_id() {
        return parseInt(this.$route.params.categorty_id);
      },
      match_id() {
        return parseInt(this.$route.params.match_id);
      },
    }
  }
