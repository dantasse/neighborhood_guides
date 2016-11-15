<template>
  <div class="nghd-list">
    <!-- A component must have one top level element, in this case the div.-->
    <ul>
      <li v-for='name in nghdNames' v-on:click='selectName(name)'>
          {{name}}
      </li>
    </ul>
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
      selectName: selectName,
      store: store
    }
  },
  computed: {
    nghdNames: function () {
      var nghdNames = store.state.neighborhoodNames[store.state.currentCity].sort()
      nghdNames.splice(nghdNames.indexOf('None'), 1)
      return nghdNames
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
li:hover {
  color: #42b983;
  cursor: pointer;
}
</style>
