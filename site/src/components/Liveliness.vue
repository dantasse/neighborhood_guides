<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    Venues per square mile:
    <div id="venuesChart" style="min-width: 310px; max-width: 960px; height: 400px; margin: 0 auto"> </div>
  </div>
</template>


<script>
import store from '../store/store.js'
import Highcharts from 'highcharts'
import { mapState } from 'vuex'

export default {
  data () {
    return {
      store: store
    }
  },
  computed: mapState({
    nghd: state => state.currentNeighborhood,
    compareNghd: state => state.compareNeighborhood
  }),
  mounted: function () {
    makeChart(store.getters.foursquareVenues, store.state)
  },
  watch: {
    nghd: function () {
      makeChart(store.getters.foursquareVenues, store.state)
    },
    compareNghd: function () {
      makeChart(store.getters.foursquareVenues, store.state)
    }
  }
}

function makeChart (venuesData, state) {
    // *sigh* just a lot of annoying protecting against nulls.
  let currentNghdData = []
  if (state.currentNeighborhood !== '') {
    let venuesPerSqMi = []
    let nghdVenues = venuesData['currentNghd']
    let area = parseFloat(nghdVenues['Area in Sq Mi'])
    venuesPerSqMi[0] = parseFloat(nghdVenues['All Venues']) / area
    venuesPerSqMi[1] = parseFloat(nghdVenues['Food']) / area
    venuesPerSqMi[2] = parseFloat(nghdVenues['Arts and Entertainment']) / area
    venuesPerSqMi[3] = parseFloat(nghdVenues['Nightlife Spot']) / area
    venuesPerSqMi[4] = parseFloat(nghdVenues['Outdoors & Recreation']) / area
    venuesPerSqMi[5] = parseFloat(nghdVenues['Shop & Service']) / area
    currentNghdData = venuesPerSqMi
  }
  let currentCityData = []
  let cityVenues = venuesData['currentCity']
  let cityArea = parseFloat(cityVenues['Area in Sq Mi'])
  currentCityData[0] = parseFloat(cityVenues['All Venues']) / cityArea
  currentCityData[1] = parseFloat(cityVenues['Food']) / cityArea
  currentCityData[2] = parseFloat(cityVenues['Arts and Entertainment']) / cityArea
  currentCityData[3] = parseFloat(cityVenues['Nightlife Spot']) / cityArea
  currentCityData[4] = parseFloat(cityVenues['Outdoors & Recreation']) / cityArea
  currentCityData[5] = parseFloat(cityVenues['Shop & Service']) / cityArea

  let compareNghdData = []
  if (state.compareNeighborhood !== '') {
    let venuesPerSqMi = []
    let nghdVenues = venuesData['compareNghd']
    let area = parseFloat(nghdVenues['Area in Sq Mi'])
    venuesPerSqMi[0] = parseFloat(nghdVenues['All Venues']) / area
    venuesPerSqMi[1] = parseFloat(nghdVenues['Food']) / area
    venuesPerSqMi[2] = parseFloat(nghdVenues['Arts and Entertainment']) / area
    venuesPerSqMi[3] = parseFloat(nghdVenues['Nightlife Spot']) / area
    venuesPerSqMi[4] = parseFloat(nghdVenues['Outdoors & Recreation']) / area
    venuesPerSqMi[5] = parseFloat(nghdVenues['Shop & Service']) / area
    compareNghdData = venuesPerSqMi
  }

  let compareCityData = []
  let compareCityVenues = venuesData['compareCity']
  cityArea = parseFloat(compareCityVenues['Area in Sq Mi'])
  compareCityData[0] = parseFloat(compareCityVenues['All Venues']) / cityArea
  compareCityData[1] = parseFloat(compareCityVenues['Food']) / cityArea
  compareCityData[2] = parseFloat(compareCityVenues['Arts and Entertainment']) / cityArea
  compareCityData[3] = parseFloat(compareCityVenues['Nightlife Spot']) / cityArea
  compareCityData[4] = parseFloat(compareCityVenues['Outdoors & Recreation']) / cityArea
  compareCityData[5] = parseFloat(compareCityVenues['Shop & Service']) / cityArea

  Highcharts.chart('venuesChart', {
    chart: {
      type: 'bar',
      renderTo: 'venuesChart'
    },
    title: { text: '' },
    xAxis: {
      categories: ['All venues', 'Food', 'Arts and entertainment', 'Nightlife', 'Outdoors and recreation', 'Shops'],
      title: { text: null }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Venues per square mile',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ' venues per square mile'
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
          format: '{point.y:,.1f}'
        }
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 80,
      floating: true,
      borderWidth: 1,
      backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: state.currentNeighborhood || ' ',
      data: currentNghdData
    }, {
      name: state.currentCity + ' average',
      data: currentCityData
    }, {
      name: state.compareNeighborhood || ' ',
      data: compareNghdData
    }, {
      name: state.compareCity + ' average',
      data: compareCityData
    }]
  })
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
table {
  width:100%;
}
</style>

