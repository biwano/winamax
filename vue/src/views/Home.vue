<template>
  <div class="home">
    Welcome to Winamax Boss. The best app to crack bets open.
    <hr/>
    <match></match>
  </div>
</template>

<script>
// @ is an alias to /src
import Match from '@/components/Match.vue'

export default {
  name: 'Home',
  components: {
    Match
  }
}
</script>
