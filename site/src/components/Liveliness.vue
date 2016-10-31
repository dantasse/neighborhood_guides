<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    Venues per square mile:
    <table>
      <tr>
        <th>Business type</th>
        <th>{{store.state.currentNeighborhood}}</th>
        <th>All of Pittsburgh</th>
      </tr>
      <tr>
        <td>All venues</td>
        <td>{{ perSqMi['all'] }}</td>
        <td>TODO</td>
      </tr>
       <tr>
        <td>Food</td>
        <td>{{ perSqMi['food'] }}</td>
        <td>TODO</td>
      </tr>
       <tr>
        <td>Arts and entertainment</td>
        <td>{{ perSqMi['arts'] }}</td>
        <td>TODO</td>
      </tr>
       <tr>
        <td>Nightlife</td>
        <td>{{ perSqMi['nightlife'] }}</td>
        <td>TODO</td>
      </tr>
       <tr>
        <td>Outdoors and recreation</td>
        <td>{{ perSqMi['outdoors'] }}</td>
        <td>TODO</td>
      </tr>
       <tr>
        <td>Shops</td>
        <td>{{ perSqMi['shop'] }}</td>
        <td>TODO</td>
      </tr>
    </table>
  </div>
</template>


<script>
import store from '../store/store.js'

export default {
  computed: {
    perSqMi () {
      let venuesPerSqMi = {}
      let nghdVenues = store.getters.foursquareVenues
      console.log(nghdVenues)
      let area = parseFloat(nghdVenues['Area in Sq Mi'])
      venuesPerSqMi['all'] = (parseFloat(nghdVenues['All Venues']) / area).toFixed(2)
      venuesPerSqMi['food'] = (parseFloat(nghdVenues['Food']) / area).toFixed(2)
      venuesPerSqMi['arts'] = (parseFloat(nghdVenues['Arts and Entertainment']) / area).toFixed(2)
      venuesPerSqMi['nightlife'] = (parseFloat(nghdVenues['Nightlife Spot']) / area).toFixed(2)
      venuesPerSqMi['outdoors'] = (parseFloat(nghdVenues['Outdoors & Recreation']) / area).toFixed(2)
      venuesPerSqMi['shop'] = (parseFloat(nghdVenues['Shop & Service']) / area).toFixed(2)
      return venuesPerSqMi
    }
  },
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

