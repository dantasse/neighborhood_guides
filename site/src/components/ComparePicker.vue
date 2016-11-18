<template>
  <div class="nghd-list">
    <h3>Compared to
      <select v-model='newCompareNghd' v-on:change='selectName(newCompareNghd)'>
        <option v-for='nghd in nghdNames'>{{nghd}}</option>
      </select>
    </h3>
  </div>
</template>


<script>
import store from '../store/store.js'

// Here we can use ES6 (ES2015) features, like 'let'.
let selectName = function (name) {
  // This is how you call a method on the store:
  store.dispatch('selectCompareNghd', name)
}
let newCompareNghd = ''
export default {
  data () {
    return {
      selectName: selectName,
      store: store,
      newCompareNghd: newCompareNghd
    }
  },
  computed: {
    nghdNames: function () {
      var nghdNames = store.state.neighborhoodNames[store.state.compareCity].slice()
      // Work on a slice copy b/c sort() mutates, which makes the property
      // compute again.
      nghdNames = nghdNames.sort()
      if (nghdNames.indexOf('None') >= 0) {
        nghdNames.splice(nghdNames.indexOf('None'), 1)
      }
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
