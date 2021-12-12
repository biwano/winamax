<template>
  <div>
    <app-nav></app-nav>
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-6">
          <div class="row">
            <div class="col-md-6">
              <sports-list @tournament="set_tournament"
              :input_sport_id="$route.params.sport_id"
              :input_category_id="$route.params.category_id"
              :input_tournament_id="$route.params.tournament_id"></sports-list>
            </div>
            <div class="col-md-6">
              <matches-list v-if="$route.params.tournament_id" @match="set_match"
                :input_match_id="$route.params.match_id"
                :query="{tournament_id: $route.params.tournament_id}"
              ></matches-list>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="home">
            <match :match_id="$route.params.match_id"></match>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import AppNav from '@/components/AppNav.vue'
import Match from '@/components/Match.vue'
import SportsList from '@/components/SportsList.vue'
import MatchesList from '@/components/MatchesList.vue'
import winamax_mixin from "@/winamax_mixin"

export default {
  name: 'Home',
  components: {
    Match, SportsList, MatchesList,AppNav
  },
  mixins: [winamax_mixin],
  methods: {
    set_tournament(tournament) {
      this.$router.push({ 
        name: 'Tournament', 
        params: { 
            sport_id: tournament.sportId,
            category_id: tournament.categoryId,
            tournament_id: tournament.tournamentId 
          }
        });
    },
    set_match(match) {
      this.$router.push({
        name: 'Match', 
        params: {
          sport_id: match.sportId, 
          category_id: match.categoryId,
          tournament_id: match.tournamentId,
          match_id: match.matchId
        }
      });
    }
  }
}
</script>
