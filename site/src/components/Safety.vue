<template>
  <div class="safety">
    <h3>Crime in {{store.state.currentNeighborhood}}</h3>
    <table>
      <tr>
        <th>Crime type</th>
        <th>Per 1000 people in <br>{{store.state.currentNeighborhood}}</th>
        <th>Per 1000 people in <br>all of Pittsburgh</th>
      </tr>
      <tr>
        <td>Part 1 crimes (most serious)</td>
        <td>{{crimeStats['Part1Per1000']}}</td>
        <td>{{cityCrimeStats['Part1Per1000']}}</td>
      </tr>
      <tr>
        <td>Part 2 crimes (less serious)</td>
        <td>{{crimeStats['Part2Per1000']}}</td>
        <td>{{cityCrimeStats['Part2Per1000']}}</td>
      </tr>
      <tr>
        <td>Total crimes</td>
        <td>{{crimeStats['TotalPer1000']}}</td>
        <td>{{cityCrimeStats['TotalPer1000']}}</td>
      </tr>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'crimeStats',
    'cityCrimeStats'
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


