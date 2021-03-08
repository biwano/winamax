<script>
import { Line, mixins  } from 'vue-chartjs'

export default {
  name: 'OutcomeChart',
  mixins: [mixins.reactiveProp, Line],
  props: ["options"],
  mounted() {
    this.renderChart(this.chartData, this.options )
  },
}
</script>
<style scoped>
</style>
