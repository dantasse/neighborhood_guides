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
    Here is the store:
    {{store.state.current_neighborhood}}
  </div>
</template>


<script>
import store from '../store'
console.log(store)
// Here we can use ES6 (ES2015) features, like 'let'.
let nghds = require('../assets/pgh_nghd_autotags.json')
let nghdNames = Object.keys(nghds)

let selectName = function (name) {
  console.log(name)
}

export default {
  data () {
    return {
      nghdNames: nghdNames,
      selectName: selectName,
      store: store
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
li {
  color: #42b983;
}
</style>
