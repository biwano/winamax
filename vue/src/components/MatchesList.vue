<template>
  <div>
    <span class="lead">{{ title }}</span
    ><br />
    <span v-show="matches.length == 0">Aucun match</span>
    <ul class="nav nav-pills  flex-column">
      <li v-for="match in matches" :key="match.matchId" class="nav-item">
        <a
          href="javascript:;"
          @click="$emit('match', match)"
          class="nav-link"
          :class="clazz(match)"
          :title="
            `${match.sport.name} - ${match.category.name} - ${match.tournament.name}`
          "
        >
          {{ label(match) }}
          <br />
          <MatchExtraInfo v-if="with_extra_info" :match="match">
            ></MatchExtraInfo
          >
          <MatchMarks :match="match"></MatchMarks>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin";
import MatchMarks from "@/components/MatchMarks";
import MatchExtraInfo from "@/components/MatchExtraInfo";

export default {
  name: "MatchesList",
  mixins: [winamax_mixin],
  props: ["query", "input_match_id", "title", "with_extra_info"],
  components: { MatchMarks, MatchExtraInfo },
  data() {
    return {
      matches: [],
    };
  },
  watch: {
    query() {
      this.load();
    },
  },
  methods: {
    async load() {
      if (this.query) {
        this.matches = await this.get(
          `/matches?query=${encodeURIComponent(JSON.stringify(this.query))}`
        );
      }
    },
    label(match) {
      return `${this.date(match.matchStart)}: ${match.competitor1Name} - ${
        match.competitor2Name
      } `;
    },
    clazz(match) {
      var res = {};
      if (match.matchId == this.input_match_id) res["active"] = true;
      if (match.mainBetId === null) res["disabled"] = true;
      return res;
    },
  },
  created() {
    this.load();
  },
};
</script>
<style scoped></style>
