<template>
  <div class="safety">
    <h3>Crime in {{store.state.currentNeighborhood}}</h3>
    <table>
      <tr>
        <th>Crime type</th>
        <th>Per 1000 people in <br>{{store.state.currentNeighborhood}}</th>
        <th>Per 1000 people in <br>{{store.state.currentCity}}</th>
        <th>Per 1000 people in <br>{{store.state.compareNeighborhood}}</th>
        <th>Per 1000 people in <br>{{store.state.compareCity}}</th>
      </tr>
      <tr>
        <td>Part 1 crimes (most serious)</td>
        <td v-if="crimeStats['currentNghd'] !== undefined">
          {{crimeStats['currentNghd']['part1_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['currentCity']['part1_per_1000_ppl']}}</td>
        <td v-if="crimeStats['compareNghd'] !== undefined">
          {{crimeStats['compareNghd']['part1_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['compareCity']['part1_per_1000_ppl']}}</td>
      </tr>
      <tr>
        <td>Part 2 crimes (less serious)</td>
        <td v-if="crimeStats['currentNghd'] !== undefined">
          {{crimeStats['currentNghd']['part2_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['currentCity']['part2_per_1000_ppl']}}</td>
        <td v-if="crimeStats['compareNghd'] !== undefined">
          {{crimeStats['compareNghd']['part2_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['compareCity']['part2_per_1000_ppl']}}</td>
      </tr>
      <tr>
        <td>Total crimes</td>
        <td v-if="crimeStats['currentNghd'] !== undefined">
          {{crimeStats['currentNghd']['total_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['currentCity']['total_per_1000_ppl']}}</td>
        <td v-if="crimeStats['compareNghd'] !== undefined">
          {{crimeStats['compareNghd']['total_per_1000_ppl']}}
        </td>
        <td v-else>No data</td>
        <td>{{crimeStats['compareCity']['total_per_1000_ppl']}}</td>
      </tr>
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


