<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link to="/" class="navbar-brand">Winamax Boss</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
      </ul>

      <ul class="navbar-nav">
        <li class="nav-item"> <router-link class="nav-link" to="/next_matches">Prochain matchs</router-link></li>
        <li class="nav-item"> <router-link class="nav-link" to="/live_matches">Matchs en cours</router-link></li>
        <li class="nav-item"> <router-link class="nav-link" to="/marked_matches">Matchs intéressants</router-link></li>
        <li class="nav-item"> <router-link class="nav-link" to="/dashboard">Dashboard</router-link></li>
      </ul>
    </div>
  </nav>

</template>

<script>

export default {
  name: 'AppNav',
}
</script>
