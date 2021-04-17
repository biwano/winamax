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

var scales = { 
  "all" : {
    label: "All",
    value: 864000000
  },
  "86400" : {
    label: "1 day",
    value: 86400
  },
  "900" : {
    label: "1 hour",
    value: 3600
  },
  "15" : {
    label: "15 minutes",
    value: 900
  }
}
export { scales }
export default {
  name: 'Outcome',
  mixins: [winamax_mixin, Line],
  props: ["outcome-id", "scale"],
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
    },
    scale() {
      this.load();
    }
  },
  methods: {
    async load() {
      this.outcome = await this.get(`/outcomes/${this.outcomeId}`);
      var history = await this.get(`/outcomes/${this.outcomeId}/history`);
      var data = []
      var labels = []
      var pointBackgroundColor = []
      var pointBorderColor = []
      var lasty = null;
      var mintime = new Date().getTime() - this.scale.value * 1000;
      history.forEach((h) => {
        var y =  h.data.odds;
        var time = h.time;
        if (time * 1000 > mintime) {
          data.push({
            time: time,
            y
          })
          var date = new Date(h.time * 1000)
          labels.push(`${date.getHours()}:${date.getMinutes()} `)
          var color = "#0000aa"
          if (lasty != null && y > lasty) color = "#00aa00"
          if (lasty != null && y < lasty) color = "#aa0000"
          pointBackgroundColor.push("rgba(0, 0, 0, 0)")
          pointBorderColor.push(color)
          lasty=y;
        }
      });
      this.chartData = {
        labels,
        datasets: [
          {
            backgroundColor: "rgba(0, 0, 0, 0)",
            borderColor: "#aaaaaa",
            label: 'Odds',
            data,
            pointBackgroundColor,
            pointBorderColor
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
