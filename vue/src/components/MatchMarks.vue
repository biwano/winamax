<template>
  <span>
    <span class="list-inline-item" v-for="mark in match.marks" :key="mark">
      <small class="badge rounded-pill bg-light">{{ mark }}</small>
    </span>
  </span>
</template>

<script>
export default {
  name: "MatchesMarks",
  props: ["match"],
};
</script>
