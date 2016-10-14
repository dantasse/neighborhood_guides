<template>
  <div class="aesthetics">
    <h3>Crime in {{store.state.currentNeighborhood}}</h3>
    <ul>
      <li>Part 1 crimes (most serious) per 1000 people: {{crimeStats['Part1Per1000']}}</li>
      <li>Part 2 crimes (less serious) per 1000 people: {{crimeStats['Part2Per1000']}}</li>
      <li>Total crimes per 1000 people: {{crimeStats['TotalPer1000']}}</li>
    </ul>
    <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'crimeStats'
  ]),
  data () {
    return {
      store: store
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>


