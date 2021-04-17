<template>
  <div>
    <div v-if="match && match.bet">
      <div class="float-right">
        <button type="button" class="btn btn-success" @click="send_mail">Prévenir Lala</button>
      </div>
      <div>
        <h6>{{ match.competitor1Name }} - {{ match.competitor2Name }}</h6>
        {{ date(match.matchStart) }}
      </div>
      <ul class="nav nav-pills">
        <li v-for="s in scales" :key="s.value" class="nav-item" 
          @click="scale = s" 
          >
          <a class="nav-link" href="javascript:;" :class="{active: s.value==scale.value}">{{s.label}}</a>
        </li>
      </ul>
      <div v-for="outcome in match.bet.outcomes" :key="outcome">
        <hr/>
        <outcome  :outcome-id="outcome" :scale="scale"></outcome>
      </div>
  </div>
  </div>

</template>

<script>
import winamax_mixin from "@/winamax_mixin"
import Outcome from "@/components/Outcome.vue"
import { scales } from "@/components/Outcome.vue"
export default {
  name: 'Match',
  mixins: [winamax_mixin],
  components: { Outcome },
  data() {
    return { 
      match: [],
      scales,
      scale: scales["all"],
    }
  },
  watch : {
    $route() {
      this.load();
    }
  },
  methods: {
    async load() {
      if (this.match_id) {
        this.match = await this.get(`/matches/${this.match_id}`);
      }
    },
    date(timestamp) {
      var date = new Date(timestamp * 1000);
      /*var date_format_str = date.getFullYear().toString()+"-"+((date.getMonth()+1).toString().length==2?(date.getMonth()+1).toString():"0"+(date.getMonth()+1).toString())+"-"+(date.getDate().toString().length==2?date.getDate().toString():"0"+date.getDate().toString())+" "+(date.getHours().toString().length==2?date.getHours().toString():"0"+date.getHours().toString())+":"+((parseInt(date.getMinutes()/5)*5).toString().length==2?(parseInt(date.getMinutes()/5)*5).toString():"0"+(parseInt(date.getMinutes()/5)*5).toString())+":00";*/
      return date;
    },
    send_mail() {
      this.post(`/matches/${this.match_id}/send_mail`);
    }
  },
  created() {
    this.load();
  }
}
</script>
<style scoped>
</style>
