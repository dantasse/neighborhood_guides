<template>
  <div class="convenience">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <div id="walkscoreChart" style="min-width: 310px; max-width: 960px; height: 400px; margin: 0 auto"> </div>
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
  if (state.compareNeighborhood !== '') {
    compareNghdData = [parseFloat(walkscores['compareNghd']['Walk Score']),
      parseFloat(walkscores['compareNghd']['Transit Score']),
      parseFloat(walkscores['compareNghd']['Bike Score'])]
  }
  let currentNghdData = []
  if (state.currentNeighborhood !== '') {
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
      valueSuffix: '',
      shared: true
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

