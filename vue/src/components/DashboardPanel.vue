<template>
  <div>
    <div class="text-right">
      <a href="javascript:;" @click="$emit('remove')"><i class="fas fa-minus-square"></i>&nbsp;</a>
    </div>
    <div v-show="match==undefined">
      <div class="row">
        <div class="col-md-6">
          <sports-list @tournament="set_tournament"></sports-list>
        </div>
        <div class="col-md-6">
          <matches-list v-if="tournament" @match="set_match"
                :query="{tournament_id: tournament.tournamentId}">
              </matches-list>
        </div>
      </div>
    </div>
    <div v-show="match!=undefined">
      <match :match_id="match_id"></match>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import SportsList from '@/components/SportsList.vue'
import MatchesList from '@/components/MatchesList.vue'
import Match from '@/components/Match.vue'

export default {
  name: 'DashboardPanel',
  data() {
    return {
      tournament: undefined,
      match: undefined
    }
  },
  methods: {
    set_tournament(tournament) {
      this.tournament = tournament
    },
    set_match(match) {
      this.match = match
    }
  },
  computed: {
    match_id() {
      return this.match ? this.match.matchId : undefined
    }
  },
  components: {
    SportsList, MatchesList, Match
  }
}
</script>
