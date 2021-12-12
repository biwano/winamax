<template>
  <div>
    <h6>Matchs</h6>
    <h6 v-show="matches.length == 0">Aucun match</h6>
    <ul  class="nav nav-pills flex-column">
      <li v-for="match in matches" :key="match.matchId" class="nav-item">
         <a href="javascript:;" @click="$emit('match', match)" class="nav-link" ::class="clazz(match)">{{ label(match) }}</a>

      </li>
    </ul>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin"
export default {
  name: 'MatchesList',
  mixins: [winamax_mixin],
  props: ["sport_id", "category_id", "tournament_id" ],
  data() {
    return { 
      matches: [],      
    }
  },
  watch : {
    tournament_id() {
      this.load();
    }
  },
  methods: {
    async load() {
      if (this.tournament_id) {
        this.matches = await this.get(`/tournaments/${this.tournament_id}/matches`);
      }
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
