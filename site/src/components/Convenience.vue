<template>
  <div class="convenience">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <table v-if="'currentNghd' in walkscores">
      <tr>
        <th></th>
        <th>{{store.state.currentNeighborhood}}</th>
        <th>{{store.state.currentCity}}</th>
        <th>{{store.state.compareNeighborhood}}</th>
        <th>{{store.state.compareCity}}</th>
      </tr>
      <tr>
        <td>Walk Score</td>
        <td>{{walkscores['currentNghd']['Walk Score']}}</td>
        <td>{{walkscores['currentCity']['Walk Score']}}</td>
        <td>{{walkscores['compareNghd']['Walk Score']}}</td>
        <td>{{walkscores['compareCity']['Walk Score']}}</td>
      </tr>
      <tr>
        <td>Transit Score</td>
        <td>{{walkscores['currentNghd']['Transit Score']}}</td>
        <td>{{walkscores['currentCity']['Transit Score']}}</td>
        <td>{{walkscores['compareNghd']['Transit Score']}}</td>
        <td>{{walkscores['compareCity']['Transit Score']}}</td>
      </tr>
      <tr>
        <td>Bike Score</td>
        <td>{{walkscores['currentNghd']['Bike Score']}}</td>
        <td>{{walkscores['currentCity']['Bike Score']}}</td>
        <td>{{walkscores['compareNghd']['Bike Score']}}</td>
        <td>{{walkscores['compareCity']['Bike Score']}}</td>
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
    'walkscores'
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



