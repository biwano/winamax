<template>
  <div>
      <h6>Sports</h6>
      <ul v-for="sport in sports" :key="sport.sportId" class="list-group">
        <!-- Sport -->
        <li class="list-group-item clickable" @click="open(sport, $event)">
          {{sport.name}}
          <!-- Category -->
          <div v-if="sport.ui_open == true">
            <ul v-for="category in sport.categories" :key="category.categoryId" class="list-group">
              <li class="list-group-item clickable" @click="open(category, $event)">
                {{category.name}}
                <!-- Tournament -->
                <div v-if="category.ui_open == true">
                  <ul v-for="tournament in category.tournaments" :key="tournament.tournamentId" class="list-group">
                    <li class="list-group-item clickable" @click="open(tournament, $event)">
                       <router-link :to="to(tournament)">{{tournament.name}}</router-link>
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
    clazz(sport) {
      var res = {}
      if (sport.sportId == this.sport_id) res["active"] = true;
      return res;
    },
    open(thing, event) {
      thing.ui_open = thing.ui_open == true ? false: true;
      this.sports = Object.assign({}, this.sports);
      event.stopPropagation();
    },
    to(tournament) {
      return { 
        name: "Tournament", 
        params: {
          sport_id: tournament["sportId"],
          category_id: tournament["categoryId"],
          tournament_id: tournament["tournamentId"]
        }
      };
    }

  },
  created() {
    this.load();
  }
}
</script>
<style scoped>
</style>
