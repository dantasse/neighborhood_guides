<template>
  <div class="convenience" id="convenience" style="display:none;">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <a href="https://www.walkscore.com/">Walkscore.com</a> has compiled scores showing how easy it is to walk, bike, or take public transit in each neighborhood.
    <div id="walkscoreChart" style="min-width: 960px; max-width: 960px; height: 400px; margin: 0 auto"> </div>
     <br/>
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
  computed: mapState({
    nghd: state => state.currentNeighborhood,
    compareNghd: state => state.compareNeighborhood
  }),
  mounted: function () {
    makeChart(store.getters.walkscores, store.state)
  },
  watch: {
    nghd: function () {
      makeChart(store.getters.walkscores, store.state)
    },
    compareNghd: function () {
      makeChart(store.getters.walkscores, store.state)
    }
  }
}

function makeChart (walkscores, state) {
    // *sigh* just a lot of annoying protecting against nulls.
  let compareNghdData = []
  if (state.compareNeighborhood !== '' && walkscores['compareNghd']) {
    compareNghdData = [parseFloat(walkscores['compareNghd']['Walk Score']),
      parseFloat(walkscores['compareNghd']['Transit Score']),
      parseFloat(walkscores['compareNghd']['Bike Score'])]
  }
  let currentNghdData = []
  if (state.currentNeighborhood !== '' && walkscores['currentNghd']) {
    currentNghdData = [parseFloat(walkscores['currentNghd']['Walk Score']),
      parseFloat(walkscores['currentNghd']['Transit Score']),
      parseFloat(walkscores['currentNghd']['Bike Score'])]
  }

  Highcharts.chart('walkscoreChart', {
    chart: {
      type: 'bar',
      renderTo: 'walkscoreChart'
    },
    title: {
      text: ''
    },
    xAxis: {
      categories: ['Walk Score', 'Transit Score', 'Bike Score'],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Scores (from walkscore.com)',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      enabled: false
//      valueSuffix: '',
//      shared: true,
//      valueDecimals: 0
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true,
          format: '{series.name}: {point.y:.0f}'
        },
        grouping: false,
        shadow: false,
        borderwidth: 0
      }
    },
    legend: {
      enabled: false
//      layout: 'vertical',
//      align: 'right',
//      verticalAlign: 'top',
//      x: -40,
//      y: 80,
//      floating: true,
//      borderWidth: 1,
//      backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
//      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: state.currentCity + ' average',
      data: [parseFloat(walkscores['currentCity']['Walk Score']),
        parseFloat(walkscores['currentCity']['Transit Score']),
        parseFloat(walkscores['currentCity']['Bike Score'])],
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
      name: state.compareCity + ' average',
      data: [parseFloat(walkscores['compareCity']['Walk Score']),
        parseFloat(walkscores['compareCity']['Transit Score']),
        parseFloat(walkscores['compareCity']['Bike Score'])],
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

