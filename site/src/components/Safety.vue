<template>
  <div class="safety">
    <h3>Crime in {{store.state.currentNeighborhood}}</h3>
    Part 1 and Part 2 crimes are defined by the FBI. <a href="https://en.wikipedia.org/wiki/Uniform_Crime_Reports#UCR_crime_categories">More info</a> <br>
    For some cities, only Part 1 crime data is available.
    <div id="crimeChart" style="min-width: 310px; max-width: 960px; height: 400px; margin: 0 auto"> </div>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapState } from 'vuex'
import Highcharts from 'highcharts'

export default {
  data () {
    return {
      store: store
    }
  },
  mounted: function () {
    makeTheChart(store.getters.crimeStats, store.state)
  },
  computed: mapState({
    nghd: state => state.currentNeighborhood,
    compareNghd: state => state.compareNeighborhood
  }),
  // So now "nghd" is an alias basically for state.currentNeighborhood, so we
  // can watch it here (using the |watch| below.)
  watch: {
    nghd: function () {
      makeTheChart(store.getters.crimeStats, store.state)
      // This means, whenever |nghd| changes (which means "whenever
      // state.currentNeighborhood changes"), call this function (remake the
      // chart.)
    },
    compareNghd: function () {
      makeTheChart(store.getters.crimeStats, store.state)
    }
  }
}

function makeTheChart (crimeStats, state) {
  // *sigh* just a lot of annoying protecting against nulls.
  let compareNghdData = []
  if (state.compareNeighborhood !== '') {
    compareNghdData = [parseFloat(crimeStats['compareNghd']['part1_per_1000_ppl']),
      parseFloat(crimeStats['compareNghd']['part2_per_1000_ppl']),
      parseFloat(crimeStats['compareNghd']['total_per_1000_ppl'])]
  }
  let currentNghdData = []
  if (state.currentNeighborhood !== '') {
    currentNghdData = [parseFloat(crimeStats['currentNghd']['part1_per_1000_ppl']),
      parseFloat(crimeStats['currentNghd']['part2_per_1000_ppl']),
      parseFloat(crimeStats['currentNghd']['total_per_1000_ppl'])]
  }

  Highcharts.chart('crimeChart', {
    chart: {
      type: 'bar',
      renderTo: 'crimeChart'
    },
    title: {
      text: ''
    },
    xAxis: {
      categories: ['Part 1 crimes (most serious)', 'Part 2 crimes (less serious)', 'Total crimes'],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Crimes per 1000 people in 2015',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ' crimes per 1000 people',
      valueDecimals: 2,
      shared: true
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
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
      name: state.currentCity,
      data: [parseFloat(crimeStats['currentCity']['part1_per_1000_ppl']),
        parseFloat(crimeStats['currentCity']['part2_per_1000_ppl']),
        parseFloat(crimeStats['currentCity']['total_per_1000_ppl'])],
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
      name: state.compareCity,
      data: [parseFloat(crimeStats['compareCity']['part1_per_1000_ppl']),
        parseFloat(crimeStats['compareCity']['part2_per_1000_ppl']),
        parseFloat(crimeStats['compareCity']['total_per_1000_ppl'])],
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


