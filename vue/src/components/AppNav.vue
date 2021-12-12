<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link to="/" class="navbar-brand">Winamax Boss</router-link>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
      </ul>

      <ul class="navbar-nav">
        <li class="nav-item"> <router-link class="nav-link" to="/next_matches">Prochain matches</router-link></li>
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
