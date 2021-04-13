<template>
  <div>
    <h6>Matches</h6>
      <ul  class="nav nav-pills flex-column">
        <li v-for="match in matches" :key="match.matchId" class="nav-item">
          <router-link 
          :to="to(match)" class="nav-link" :class="clazz(match)">{{ label(match) }} </router-link>
        </li>
      </ul>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin"
export default {
  name: 'MatchesList',
  mixins: [winamax_mixin],
  data() {
    return { 
      matches: []
    }
  },
  watch : {
    $route() {
      this.load();
    }
  },
  methods: {
    async load() {
      if (this.tournament_id) {
        this.matches = await this.get(`/tournaments/${this.tournament_id}/matches`);
      }
    },
    to(match) {
      return {name: 'Match', params: {sport_id: this.sport_id, match_id: match.matchId}}
    },
    label(match) {
      return `${match.competitor1Name} ${match.competitor2Name} `
    },
    clazz(match) {
      var res = {}
      if (match.matchId == this.match_id) res["active"] = true;
      if (match.mainBetId === null) res["disabled"] = true;
      return res;
    }

  },
  created() {
    this.load();
    window.setInterval(() => {
      this.load();
    }, 10000);
  }
}
</script>
<style scoped>
</style>
