<template>
  <div>
      <span class="lead">Tournois</span>
      <div class="form-check">
        <!--
        <input class="form-check-input" type="checkbox" v-model="only_favorites" />
        <label class="form-check-label" for="flexCheckDefault">
        Only favorites
        </label>
      -->
      </div>
      <ul v-for="sport in sports" :key="sport.sportId" class="nav nav-pills">
        <!-- Sport -->
        <li v-show="sport.matches" class="nav-item clickable" @click="open(sport, $event)">
          <span style="font-weight: 1000">{{sport.name}} ({{sport.matches}})</span>
          <!-- Category -->
          <div v-show="sport.ui_open == true" class="child">
            <ul v-for="category in sport.categories" :key="category.categoryId" class="nav nav-pills">
              <li v-show="category.matches" class="nav-item clickable" @click="open(category, $event)" style="list-style:circle">
                {{category.name}} ({{category.matches}})
                <!-- Tournament -->
                <div v-show="category.ui_open == true" @click.stop="" class="child">
                  <ul v-for="tournament in category.tournaments" :key="tournament.tournamentId" class="nav nav-pills">
                    <li v-show="tournament.matches" class="nav-item clickable" :class="clazz(tournament)" style="list-style:square">
                       <!--<input class="form-check-input" type="checkbox" v-model="tournament.favorite" @click.stop="switch_favorite(tournament)"/>-->
                       <a href="javascript:;" @click="$emit('tournament', tournament)" style="text-decoration: none">{{tournament.name}} ({{tournament.matches}})</a>
                    </li>
                  </ul>
                </div>
              </li>
            </ul>
          </div>
        </li>
      </ul>
  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin"
export default {
  name: 'SportsList',
  mixins: [winamax_mixin],
  props: [
    "input_sport_id",
    "input_category_id",
    "input_tournament_id"
  ],
  data() {
    return { 
      sports: [],
      only_favorites: false
    }
  },
  watch : {
    only_favorites() {
      this.prepare();
    }
  },
  methods: {
    async load() {
      this.sports = await this.get("/sports");
      this.prepare()
    },
    sort(array) {
      const k = "matches";
      return array.sort((a, b) => 
        a[k] == b[k] ? 0 : a[k] < b[k] ? 1 : -1);
    },
    prepare() {
      this.sort(this.sports);
      for (let sport of this.sports) {
        if (sport.id == this.input_sport_id) sport.ui_open = true;
        sport.favorite = false;
        for (let category of sport.categories) {
          if (category.id == this.input_category_id) category.ui_open = true;
          category.favorite = false;
          this.sort(category.tournaments);
          for (let tournament of category.tournaments) {
            if (tournament.favorite) { 
              category.favorite = true;
              sport.favorite = true;
            }
          }
        }
      }
      this.sports = [...this.sports]
    },
    clazz(tournament) {
      var res = {}
      if (tournament.tournamentId == this.input_tournament_id) res["active"] = true;
      return res;
    },
    open(thing, event) {
      thing.ui_open = thing.ui_open == true ? false: true;
      this.sports = [...this.sports]
      event.stopPropagation();
    },
    switch_favorite(tournament) {
      tournament.favorite = ! tournament.favorite;
      this.prepare();
      this.post(`/tournaments/${tournament.sportId}/${tournament.categoryId}/${tournament.tournamentId}`, 
        { favorite: tournament.favorite});
    },
  },
  created() {
    this.load();
  }
}
</script>
<style scoped>
  .child {
      margin-left:25px;
  }
</style>
