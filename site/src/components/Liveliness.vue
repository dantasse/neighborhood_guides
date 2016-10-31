<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    <ul>
      <li>Venues per Square Mile: {{ perSqMi['all'] }}</li>
      <li>Food venues per Square Mile: {{ perSqMi['food'] }}</li>
      <li>Arts and entertainment venues per Square Mile: {{ perSqMi['arts'] }}</li>
      <li>Nightlife venues per Square Mile: {{ perSqMi['nightlife'] }}</li>
      <li>Outdoors and recreation venues per Square Mile: {{ perSqMi['outdoors'] }}</li>
      <li>Shop venues per Square Mile: {{ perSqMi['shop'] }}</li>
    </ul>
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

</style>

