<template>
  <div class="city-picker">
    <div id='compare_city'>
      <span class='header'>I know:</span>
      <span class='city-name' v-for='city in store.state.cityList'
        v-bind:class="{selected: city === store.state.compareCity}"
        v-on:click="store.dispatch('selectCompareCity', city)">{{city}}</span>
    </div>
    <div id='current_city'>
      <span class='header'>I want to learn about:</span>
      <span class='city-name' v-for='city in store.state.cityList'
        v-bind:class="{selected: city === store.state.currentCity}"
        v-on:click="store.dispatch('selectCurrentCity', city)">{{city}}</span>
    </div>
  </div>
</template>


<script>
import store from '../store/store.js'

export default {
  data () {
    return {
      store: store
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
span {
  font-size: 16pt;
}
.city-name {
  padding: 3px 10px;
  cursor: pointer;
}
.selected {
  background-color: #000;
  color: #fff;
}
</style>
