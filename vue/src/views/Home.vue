<template>
  <div>
    <app-nav></app-nav>
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-6">
          <div class="row">
            <div class="col-md-6">
              <sports-list @tournament="navigate_tournament"></sports-list>
            </div>
            <div class="col-md-6">
              <matches-list @match="navigate_match"
                :sport_id="route_sport_id"
                :category_id="route_category_id"
                :tournament_id="route_tournament_id"
              ></matches-list>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="home">
            <match :match_id="route_match_id"></match>
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
    navigate_tournament(tournament) {
      this.$router.push({ 
        name: 'Tournament', 
        params: { 
            sport_id: tournament.sportId,
            category_id: tournament.categoryId,
            tournament_id: tournament.tournamentId 
          }
        });
    },
    navigate_match(match) {
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
