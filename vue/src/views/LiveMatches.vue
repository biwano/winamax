<template>
  <div>
    <app-nav></app-nav>
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-4">
          <matches-list
            @match="set_match"
            title="Matchs en cours"
            :input_match_id="match_id"
            :query="{ status: 'LIVE' }"
            :with_extra_info="true"
          ></matches-list>
        </div>
        <div class="col-md-8">
          <match :match_id="match_id"></match>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin";
import AppNav from "@/components/AppNav.vue";
import Match from "@/components/Match.vue";
import MatchesList from "@/components/MatchesList.vue";
export default {
  name: "LiveMatches",
  mixins: [winamax_mixin],
  components: { AppNav, Match, MatchesList },
  data() {
    return {
      match_id: undefined,
    };
  },
  methods: {
    set_match(match) {
      this.match_id = match.matchId;
    },
  },
};
</script>
<style scoped></style>
