<template>
  <div class="nghd-list">
      Here are the neighborhoods:
    <!-- A component must have one top level element, in this case the div.-->
    <ul>
      <li v-for='name in nghdNames' v-on:click='selectName(name)'>
          {{name}}
      </li>
    </ul>
    <br/>

    Here is the current neighborhood:
    {{store.state.currentNeighborhood}}
  </div>
</template>


<script>
import store from '../store/store.js'

// Here we can use ES6 (ES2015) features, like 'let'.
let selectName = function (name) {
  // This is how you call a method on the store:
  store.dispatch('selectNeighborhood', name)
}

export default {
  data () {
    return {
      nghdNames: store.state.neighborhoodNames,
      selectName: selectName,
      store: store
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
li:hover {
  color: #42b983;
}
</style>
