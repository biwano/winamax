<template>
  <div>
      <h6>Sports</h6>
      <ul v-for="sport in sports" :key="sport.sportId" class="nav nav-pills flex-column">
        <li class="nav-item">
          <router-link :to="to(sport)" class="nav-link" :class="clazz(sport)">{{sport.sportName}}</router-link>
        </li>
      </ul>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin"
export default {
  name: 'SportsList',
  mixins: [winamax_mixin],
  props: {
    msg: String
  },
  data() {
    return { 
      sports: []
    }
  },
  methods: {
    async load() {
      this.sports = await this.get("/sports");
    },
    to(sport) {
      return {name: 'Sport', params: {sport_id: sport.sportId}}
    },
    clazz(sport) {
      var res = {}
      if (sport.sportId == this.sport_id) res["active"] = true;
      return res;
    }

  },
  created() {
    this.load();
  }
}
</script>
<style scoped>
</style>
