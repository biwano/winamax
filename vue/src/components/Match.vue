<template>
  <div>
    <div v-if="match && match.bet">
      <div class="float-right text-right">
        <a @click="send_mail" href="javascript:;"
          ><i class="fas fa-envelope"></i>&nbsp;Prévenir Lala</a
        ><br />
        <a
          :href="`https://www.winamax.fr/paris-sportifs/match/${match_id}`"
          target="_blank"
          ><img
            src="https://operator-front-static-cdn.winamax.fr/img/style/v2/common/logo-highlight.png"
            height="32px"
        /></a>
      </div>
      <div>
        <span class="lead"
          >{{ match.competitor1Name }} - {{ match.competitor2Name }}</span
        ><br />
        &nbsp; <MatchExtraInfo :match="match"></MatchExtraInfo>
        <br />
        <i class="fas fa-calendar"></i>&nbsp;{{ date(match.matchStart) }}
        <br />
        <MatchMarks :match="match"></MatchMarks>
      </div>
      <hr />
      <div class="d-inline-flex">
        <i class="fas fa-cog" style="margin:auto;"></i>
        <ul class="nav nav-pills">
          <li
            v-for="s in scales"
            :key="s.value"
            class="nav-item"
            @click="scale = s"
          >
            <a
              class="nav-link"
              href="javascript:;"
              :class="{ active: s.value == scale.value }"
              >{{ s.label }}</a
            >
          </li>
        </ul>
      </div>
      <div v-for="outcome in match.bet.outcomes" :key="outcome">
        <hr />
        <outcome :outcome-id="outcome" :scale="scale"></outcome>
      </div>
    </div>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin";
import Outcome from "@/components/Outcome.vue";
import MatchMarks from "@/components/MatchMarks";
import MatchExtraInfo from "@/components/MatchExtraInfo";
import { scales } from "@/components/Outcome.vue";
export default {
  name: "Match",
  mixins: [winamax_mixin],
  props: ["match_id"],
  components: { Outcome, MatchMarks, MatchExtraInfo },
  data() {
    return {
      match: [],
      scales,
      scale: scales["all"],
    };
  },
  watch: {
    match_id() {
      this.load();
    },
  },
  methods: {
    async load() {
      if (this.match_id) {
        this.match = await this.get(`/matches/${this.match_id}`);
      }
    },
    send_mail() {
      this.post(`/matches/${this.match_id}/send_mail`);
    },
    embed() {
      var copyText = `<iframe src="http://winamax.ilponse.com/#/embed/${this.sport_id}/${this.category_id}/${this.tournament_id}/${this.match_id}" height="1000px" frameBorder="0"></iframe>`;
      navigator.clipboard.writeText(copyText);
    },
  },
  created() {
    this.load();
    window.setInterval(() => {
      this.load();
    }, 60000);
  },
};
</script>
<style scoped></style>
