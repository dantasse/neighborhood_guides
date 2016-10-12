<template>
  <div class="nghd-list">
    <!--Must have one top level element, in this case the div.-->
    <ul>
      <!--<li v-for='nghd in nghds'>-->
        <!--{{nghd['autotags_90plus']}}-->
      <!--</li>-->
      <li v-for='name in nghdNames'>
          {{name}}
      </li>
    </ul>
    <br/>
    A list of neighborhoods!
  </div>
</template>


<script>
// Here we can use ES6 (ES2015) features, like 'let'.
let nghds = require('../assets/pgh_nghd_autotags.json')
let nghdNames = Object.keys(nghds)
console.log(nghdNames)

export default {
  data () {
    return {
      // nghds: nghds,
      nghdNames: nghdNames
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
