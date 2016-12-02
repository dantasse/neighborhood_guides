<template>
  <div class="nghd-list">
    <!-- A component must have one top level element, in this case the div.-->
    <h4>Particularly, this neighborhood:
      <select v-model='currentNghd' v-on:change='selectName'>
        <option value="" disabled>Select a Neighborhood</option>
        <option v-for='nghd in nghdNames' :value='nghd'>{{nghd}}</option>
      </select>
    </h4>
  </div>
</template>


<script>
import store from '../store/store.js'

// Here we can use ES6 (ES2015) features, like 'let'.
let selectName = function (ev) {
  var selectedNghd = ev.target.value
  // This is how you call a method on the store:
  store.dispatch('selectNeighborhood', selectedNghd)
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
      var nghdNames = store.state.neighborhoodNames[store.state.currentCity].slice()
      // slice() is so we have a copy, not editing the names.
      nghdNames = nghdNames.sort().filter(function (x) { return x !== 'None' })
      return nghdNames
    },
    // Computed properties are cached based on their dependencies.
    currentNghd: function () { return store.state.currentNeighborhood }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
