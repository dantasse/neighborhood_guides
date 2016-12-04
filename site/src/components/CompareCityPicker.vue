<template>
  <div class="compare-city-picker">
    <div id='compare_city'>
      <h3>I know:
        <span class='city-name' v-for='city in store.state.cityList'
          v-bind:class="{selected: city === store.state.compareCity}"
          v-on:click="store.dispatch('selectCompareCity', city)">{{city}}</span>
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

