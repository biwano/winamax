<template>
  <div>
    <app-nav></app-nav>
    <div class="container-fluid">
      <a href="javascript:;" @click="add_panel()"><i class="fas fa-plus-circle"></i>&nbsp;Ajouter un panneau</a>
      <div class="row">
        <div v-for="panel in panels"  :key="panel" :class="`col-md-${panel_class}`">
          <dashboard-panel></dashboard-panel>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
// @ is an alias to /src
import AppNav from '@/components/AppNav.vue'
import DashboardPanel from '@/components/DashboardPanel.vue'

export default {
  name: 'Dashboard',
  data() {
    return {
      panels: [],
      panel_id: 0
    }
  },
  methods: {
    add_panel() {
      this.panels.push(this.panel_id);
      this.panel_id++;
    }
  },
  computed: {
    panel_class() {
      if (this.panels.length <= 1) return 12;
      if (this.panels.length == 2) return 6;
      return 4;
    }
  },
  components: {
    AppNav, DashboardPanel
  }
}
</script>
