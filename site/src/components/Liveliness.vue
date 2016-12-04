<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    Venues per square mile:
    <table>
      <tr>
        <th>Business type</th>
        <th>{{store.state.currentNeighborhood}}</th>
        <th>All of {{store.state.currentCity}}</th>
        <th>{{store.state.compareNeighborhood}}</th>
        <th>All of {{store.state.compareCity}}</th>
      </tr>
      <tr>
        <td>All venues</td>
        <td>{{ perSqMi['all'] }}</td>
        <td>{{ cityPerSqMi['all'] }}</td>
        <td>{{ compareNghdPerSqMi['all'] }}</td>
        <td>{{ compareCityPerSqMi['all'] }}</td>
      </tr>
       <tr>
        <td>Food</td>
        <td>{{ perSqMi['food'] }}</td>
        <td>{{ cityPerSqMi['food'] }}</td>
        <td>{{ compareNghdPerSqMi['food'] }}</td>
        <td>{{ compareCityPerSqMi['food'] }}</td>
      </tr>
       <tr>
        <td>Arts and entertainment</td>
        <td>{{ perSqMi['arts'] }}</td>
        <td>{{ cityPerSqMi['arts'] }}</td>
        <td>{{ compareNghdPerSqMi['arts'] }}</td>
        <td>{{ compareCityPerSqMi['arts'] }}</td>
      </tr>
       <tr>
        <td>Nightlife</td>
        <td>{{ perSqMi['nightlife'] }}</td>
        <td>{{ cityPerSqMi['nightlife'] }}</td>
        <td>{{ compareNghdPerSqMi['nightlife'] }}</td>
        <td>{{ compareCityPerSqMi['nightlife'] }}</td>
      </tr>
       <tr>
        <td>Outdoors and recreation</td>
        <td>{{ perSqMi['outdoors'] }}</td>
        <td>{{ cityPerSqMi['outdoors'] }}</td>
        <td>{{ compareNghdPerSqMi['outdoors'] }}</td>
        <td>{{ compareCityPerSqMi['outdoors'] }}</td>
      </tr>
       <tr>
        <td>Shops</td>
        <td>{{ perSqMi['shop'] }}</td>
        <td>{{ cityPerSqMi['shop'] }}</td>
        <td>{{ compareNghdPerSqMi['shop'] }}</td>
        <td>{{ compareCityPerSqMi['shop'] }}</td>
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
      let nghdVenues = store.getters.foursquareVenues['currentNghd']
      if (nghdVenues === undefined) {
        return {'all': 'No Data', 'food': 'No Data', 'arts': 'No Data', 'nightlife': 'No Data', 'outdoors': 'No Data', 'shop': 'No Data'}
      }
      let area = parseFloat(nghdVenues['Area in Sq Mi'])
      venuesPerSqMi['all'] = (parseFloat(nghdVenues['All Venues']) / area).toFixed(2)
      venuesPerSqMi['food'] = (parseFloat(nghdVenues['Food']) / area).toFixed(2)
      venuesPerSqMi['arts'] = (parseFloat(nghdVenues['Arts and Entertainment']) / area).toFixed(2)
      venuesPerSqMi['nightlife'] = (parseFloat(nghdVenues['Nightlife Spot']) / area).toFixed(2)
      venuesPerSqMi['outdoors'] = (parseFloat(nghdVenues['Outdoors & Recreation']) / area).toFixed(2)
      venuesPerSqMi['shop'] = (parseFloat(nghdVenues['Shop & Service']) / area).toFixed(2)
      return venuesPerSqMi
    },
    cityPerSqMi () {
      let cityVenuesPerSqMi = {}
      let cityVenues = store.getters.foursquareVenues['currentCity']
      cityVenuesPerSqMi['all'] = parseFloat(cityVenues['All Venues']).toFixed(2)
      cityVenuesPerSqMi['food'] = parseFloat(cityVenues['Food']).toFixed(2)
      cityVenuesPerSqMi['arts'] = parseFloat(cityVenues['Arts and Entertainment']).toFixed(2)
      cityVenuesPerSqMi['nightlife'] = parseFloat(cityVenues['Nightlife Spot']).toFixed(2)
      cityVenuesPerSqMi['outdoors'] = parseFloat(cityVenues['Outdoors & Recreation']).toFixed(2)
      cityVenuesPerSqMi['shop'] = parseFloat(cityVenues['Shop & Service']).toFixed(2)
      return cityVenuesPerSqMi
    },
    compareNghdPerSqMi () {
      let venuesPerSqMi = {}
      let nghdVenues = store.getters.foursquareVenues['compareNghd']
      if (nghdVenues === undefined) {
        return {'all': 'No Data', 'food': 'No Data', 'arts': 'No Data', 'nightlife': 'No Data', 'outdoors': 'No Data', 'shop': 'No Data'}
      }
      let area = parseFloat(nghdVenues['Area in Sq Mi'])
      venuesPerSqMi['all'] = (parseFloat(nghdVenues['All Venues']) / area).toFixed(2)
      venuesPerSqMi['food'] = (parseFloat(nghdVenues['Food']) / area).toFixed(2)
      venuesPerSqMi['arts'] = (parseFloat(nghdVenues['Arts and Entertainment']) / area).toFixed(2)
      venuesPerSqMi['nightlife'] = (parseFloat(nghdVenues['Nightlife Spot']) / area).toFixed(2)
      venuesPerSqMi['outdoors'] = (parseFloat(nghdVenues['Outdoors & Recreation']) / area).toFixed(2)
      venuesPerSqMi['shop'] = (parseFloat(nghdVenues['Shop & Service']) / area).toFixed(2)
      return venuesPerSqMi
    },
    compareCityPerSqMi () {
      let cityVenuesPerSqMi = {}
      let cityVenues = store.getters.foursquareVenues['compareCity']
      cityVenuesPerSqMi['all'] = parseFloat(cityVenues['All Venues']).toFixed(2)
      cityVenuesPerSqMi['food'] = parseFloat(cityVenues['Food']).toFixed(2)
      cityVenuesPerSqMi['arts'] = parseFloat(cityVenues['Arts and Entertainment']).toFixed(2)
      cityVenuesPerSqMi['nightlife'] = parseFloat(cityVenues['Nightlife Spot']).toFixed(2)
      cityVenuesPerSqMi['outdoors'] = parseFloat(cityVenues['Outdoors & Recreation']).toFixed(2)
      cityVenuesPerSqMi['shop'] = parseFloat(cityVenues['Shop & Service']).toFixed(2)
      return cityVenuesPerSqMi
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

