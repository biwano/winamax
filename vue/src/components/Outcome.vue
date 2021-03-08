<template>
  <div>
    <h6>
    {{ outcome.label }}: {{ outcome.percentDistribution }}%</h6> 
    
    <outcome-chart 
      :outcome-id="outcomeId" 
      class=""
      :options="{
        aspectRatio: 2, 
        responsive: true,  
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
              display: true,
              ticks: {
                  beginAtZero: true   // minimum value will be 0.
              }
          }]
        }
      }"
      :chartData="chartData"
      style="height: 200px; position: relative"
    ></outcome-chart>

  </div>
</template>

<script>
import winamax_mixin from "@/winamax_mixin"
import { Line } from 'vue-chartjs'
import OutcomeChart from './OutcomeChart.vue'
export default {
  name: 'Outcome',
  mixins: [winamax_mixin, Line],
  props: ["outcome-id"],
  components: { OutcomeChart },
  data() {
    return { 
      outcome: {},
      chartData: {}
    }
  },
  watch : {
    $route() {
      this.load();
    }
  },
  methods: {
    async load() {
      this.outcome = await this.get(`/outcomes/${this.outcomeId}`);
      var history = await this.get(`/outcomes/${this.outcomeId}/history`);
      var data = []
      var labels = []
      history.forEach((h) => {
        data.push({
          time: h.time,
          y: h.data.odds
        })
        var date = new Date(h.time * 1000)
        labels.push(`${date.getHours()}:${date.getMinutes()} `)
      });
      this.chartData = {
          labels,
          datasets: [
            {
              backgroundColor: "rgba(0, 0, 0, 0)",
              label: 'Odds',
              data
            }
          ]
        }
      
    }
  },
  created() {
    this.load();
  }
}
</script>
<style scoped>
.chart {
  max-height: 200px;
}
</style>
