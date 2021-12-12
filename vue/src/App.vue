<template>
  <div>
    <router-view/>
  </div>
</template>
<script>

export default {
  name: 'App'
}
</script>

<style>
.clickable {
  cursor:pointer;  
}
.list-group-item.active a {
  color: #fff;
}
.float-right {
  float: right;
}
.text-right {
  text-align: right;
}
</style>
