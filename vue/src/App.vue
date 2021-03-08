<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      Winamax Boss
    </nav>
      
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-6">
          <div class="row">
            <div class="col-md-6">
              <sports-list></sports-list>
            </div>
            <div class="col-md-6">
              <matches-list></matches-list>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <router-view/>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import SportsList from '@/components/SportsList.vue'
import MatchesList from '@/components/MatchesList.vue'

export default {
  name: 'App',
  components: {
    SportsList, MatchesList
  }
}
</script>

<style>

</style>
