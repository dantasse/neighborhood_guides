<template>
  <div class="convenience">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <table>
      <tr>
        <th></th>
        <th>{{store.state.currentNeighborhood}}</th>
        <th>{{store.state.currentCity}} Average</th>
        <th>{{store.state.compareNeighborhood}}</th>
        <th>{{store.state.compareCity}} Average</th>
      </tr>
      <tr>
        <td>Walk Score</td>
        <td v-if="walkscores['currentNghd'] !== undefined">{{walkscores['currentNghd']['Walk Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['currentCity']['Walk Score']}}</td>
        <td v-if="walkscores['compareNghd'] !== undefined">{{walkscores['compareNghd']['Walk Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['compareCity']['Walk Score']}}</td>
      </tr>
      <tr>
        <td>Transit Score</td>
        <td v-if="walkscores['currentNghd'] !== undefined">{{walkscores['currentNghd']['Transit Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['currentCity']['Transit Score']}}</td>
        <td v-if="walkscores['compareNghd'] !== undefined">{{walkscores['compareNghd']['Transit Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['compareCity']['Transit Score']}}</td>
      </tr>
      <tr>
        <td>Bike Score</td>
        <td v-if="walkscores['currentNghd'] !== undefined">{{walkscores['currentNghd']['Bike Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['currentCity']['Bike Score']}}</td>
        <td v-if="walkscores['compareNghd'] !== undefined">{{walkscores['compareNghd']['Bike Score']}}</td>
        <td v-else></td>
        <td>{{walkscores['compareCity']['Bike Score']}}</td>
      </tr>
    </table>
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
table {
  width:100%;
}
</style>

