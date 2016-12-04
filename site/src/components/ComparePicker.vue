<template>
  <div class="compare-picker">
    <h4>I know this neighborhood:
      <select v-model='compareNghd' v-on:change='selectName'>
        <option value="" disabled>Select a Neighborhood</option>
        <option v-for='nghd in nghdNames' :value='nghd'>{{nghd}}</option>
      </select>
    </h4>
  </div>
</template>


<script>
import store from '../store/store.js'

let selectName = function (ev) {
  var selectedNghd = ev.target.value
  store.dispatch('selectCompareNghd', selectedNghd)
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
      var nghdNames = store.state.neighborhoodNames[store.state.compareCity].slice()
      // Work on a slice copy b/c sort() mutates, which makes the property
      // compute again.
      nghdNames = nghdNames.sort().filter(function (x) { return x !== 'None' })
      return nghdNames
    },
    compareNghd: function () { return store.state.compareNeighborhood }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
