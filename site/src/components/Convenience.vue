<template>
  <div class="convenience">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <table v-if="'Walk Score' in walkscores">
      <tr>
        <th></th>
        <th>{{store.state.currentNeighborhood}}</th>
        <th>{{store.state.currentCity}}</th>
      </tr>
      <tr>
        <td>Walk Score</td>
        <td>{{walkscores['Walk Score']}}</td>
        <td>{{cityWalkscores['Walk Score']}}</td>
      </tr>
      <tr>
        <td>Transit Score</td>
        <td>{{walkscores['Transit Score']}}</td>
        <td>{{cityWalkscores['Transit Score']}}</td>
      </tr>
      <tr>
        <td>Bike Score</td>
        <td>{{walkscores['Bike Score']}}</td>
        <td>{{cityWalkscores['Bike Score']}}</td>
      </tr>
    </table>
    <div v-else>
      No data for {{store.state.currentNeighborhood}}
    </div>
     <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'walkscores',
    'cityWalkscores'
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



