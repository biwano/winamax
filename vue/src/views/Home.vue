<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <h4>Winamax Boss: The best app to crack bets open.</h4>
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
          <div class="home">
            <match></match>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Match from '@/components/Match.vue'
import SportsList from '@/components/SportsList.vue'
import MatchesList from '@/components/MatchesList.vue'

export default {
  name: 'Home',
  components: {
    Match, SportsList, MatchesList

  }
}
</script>
