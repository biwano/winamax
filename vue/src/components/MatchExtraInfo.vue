<template>
  <small>
    <i
      >{{ match.sport.name }} - {{ match.category.name }} -
      {{ match.tournament.name }}</i
    >
  </small>
</template>

<script>
export default {
  name: "MatchesExtraInfo",
  props: ["match"],
};
</script>
