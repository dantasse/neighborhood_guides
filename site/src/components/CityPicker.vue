<template>
  <div class="current-city-picker">
    <div id='current_city'>
      <h3>I want to learn about:
        <span class='city-name' v-for='city in store.state.cityList'
          v-bind:class="{selected: city === store.state.currentCity}"
          v-on:click="store.dispatch('selectCurrentCity', city)">{{city}}</span>
      </h3>
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
.city-name {
  padding: 3px 10px;
  cursor: pointer;
}
.selected {
  background-color: #000;
  color: #fff;
}
</style>
