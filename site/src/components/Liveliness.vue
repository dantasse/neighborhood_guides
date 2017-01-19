<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    Venues per square mile (via Foursquare):
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
    venuesPerSqMi[0] = parseFloat(nghdVenues['All Venues'])
    venuesPerSqMi[1] = parseFloat(nghdVenues['Food'])
    venuesPerSqMi[2] = parseFloat(nghdVenues['Arts and Entertainment'])
    venuesPerSqMi[3] = parseFloat(nghdVenues['Nightlife Spot'])
    venuesPerSqMi[4] = parseFloat(nghdVenues['Outdoors & Recreation'])
    venuesPerSqMi[5] = parseFloat(nghdVenues['Shop & Service'])
    currentNghdData = venuesPerSqMi
  }
  let currentCityData = []
  let cityVenues = venuesData['currentCity']
  currentCityData[0] = parseFloat(cityVenues['All Venues'])
  currentCityData[1] = parseFloat(cityVenues['Food'])
  currentCityData[2] = parseFloat(cityVenues['Arts and Entertainment'])
  currentCityData[3] = parseFloat(cityVenues['Nightlife Spot'])
  currentCityData[4] = parseFloat(cityVenues['Outdoors & Recreation'])
  currentCityData[5] = parseFloat(cityVenues['Shop & Service'])

  let compareNghdData = []
  if (state.compareNeighborhood !== '') {
    let venuesPerSqMi = []
    let nghdVenues = venuesData['compareNghd']
    venuesPerSqMi[0] = parseFloat(nghdVenues['All Venues'])
    venuesPerSqMi[1] = parseFloat(nghdVenues['Food'])
    venuesPerSqMi[2] = parseFloat(nghdVenues['Arts and Entertainment'])
    venuesPerSqMi[3] = parseFloat(nghdVenues['Nightlife Spot'])
    venuesPerSqMi[4] = parseFloat(nghdVenues['Outdoors & Recreation'])
    venuesPerSqMi[5] = parseFloat(nghdVenues['Shop & Service'])
    compareNghdData = venuesPerSqMi
  }

  let compareCityData = []
  let compareCityVenues = venuesData['compareCity']
  compareCityData[0] = parseFloat(compareCityVenues['All Venues'])
  compareCityData[1] = parseFloat(compareCityVenues['Food'])
  compareCityData[2] = parseFloat(compareCityVenues['Arts and Entertainment'])
  compareCityData[3] = parseFloat(compareCityVenues['Nightlife Spot'])
  compareCityData[4] = parseFloat(compareCityVenues['Outdoors & Recreation'])
  compareCityData[5] = parseFloat(compareCityVenues['Shop & Service'])

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
      shared: true,
      valueSuffix: ' venues per square mile',
      valueDecimals: 0
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
          format: '{point.y:,.0f}'
        },
        grouping: false,
        shadow: false,
        borderwidth: 0
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
      name: state.currentCity + ' median neighborhood',
      data: currentCityData,
      color: 'rgba(165,170,217,1)',
      pointPadding: 0.3,
      pointPlacement: 0.15
    }, {
      name: state.currentNeighborhood || ' ',
      data: currentNghdData,
      color: 'rgba(126,86,134,.9)',
      pointPadding: 0.4,
      pointPlacement: 0.15
    }, {
      name: state.compareCity + ' median neighborhood',
      data: compareCityData,
      color: 'rgba(248,161,63,1)',
      pointPadding: 0.3,
      pointPlacement: -0.15
    }, {
      name: state.compareNeighborhood || ' ',
      data: compareNghdData,
      color: 'rgba(186,60,61,.9)',
      pointPadding: 0.4,
      pointPlacement: -0.15
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

