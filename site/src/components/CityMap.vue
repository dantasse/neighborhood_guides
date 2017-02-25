<template>
  <div class="city-map">
    <div>
      <select id="map_picker" v-model="currentMap" v-on:change='setCurrentMap'>
        <option value='Neighborhood Bounds'>Neighborhood Bounds</option>
        <option value='Total Crime'>Total Crime</option>
        <option value='Part 1 Crime'>Part 1 (more serious) crime</option>
        <option value='Part 2 Crime'>Part 2 (less serious) crime</option>
        <option value='Walk Score'>Walk Score</option>
        <option value='Bike Score'>Bike Score</option>
        <option value='Transit Score'>Transit Score</option>
        <option value='Arts Venues'>Arts Venues</option>
        <option value='Nightlife Venues'>Nightlife Venues</option>
        <option value='Shops'>Shops</option>
        <option value='Outdoor and Recreation Venues'>Outdoor and Recreation Venues</option>
        <option value='Food Venues'>Food Venues</option>
        <option value='All Venues'>All Venues</option>
      </select>

    </div>
    <div id='leafletMap'>
    </div>
  </div>
</template>


<script>
// import Vue from 'vue'
import store from '../store/store.js'
import L from 'leaflet'

// Define this here so we can reference it in setUpMap and resetHighlight.
var geojsonLayer
var infoBox
// var mapPicker // Control to say whether we want to look at crime, walkscores, etc.
// let currentMap = ['foo'] // which one we're looking at now.
var map

var mapFeatures = {}

let setCurrentMap = function (e) {
  var selectedMap = e.target.value
  store.dispatch('setCurrentMap', selectedMap)
}

function addHandlers (feature, layer) {
  layer.on({
    click: selectNghd,
    mouseover: highlightFeature,
    mouseout: resetHighlight
  })
  mapFeatures[feature['properties']['name']] = layer
}

function selectNghd (e) {
  let nghd = e.target.feature.properties.name
  store.dispatch('selectNeighborhood', nghd)
}

function highlightFeature (e) {
  var layer = e.target
  doHighlight(layer)
}
function doHighlight (layer) {
  layer.setStyle({
    weight: 5,
    color: '#666',
    dashArray: '',
    fillOpacity: 0.7
  })

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
    layer.bringToFront()
  }
  infoBox.update(layer.feature.properties['name'], store.state.currentMap)
}
function resetHighlight (e) {
  geojsonLayer.resetStyle(e.target)
  infoBox.update()
}

function setUpMap (latlon, neighborhoodsGeojson) {
  map = L.map('leafletMap', {
    minZoom: 11,
    maxZoom: 16,
    inertia: false
  })
  map.setView([latlon[0], latlon[1]], zoomLevel)
  //
  L.tileLayer('http://a.tiles.mapbox.com/v4/mapbox.light/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZGFudGFzc2UiLCJhIjoiWkpJVUNjSSJ9.EEaUQpuPDkOhI8rX4ihVDQ', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18
  }).addTo(map)
  geojsonLayer = L.geoJSON(neighborhoodsGeojson, {
    style: geojsonStyle,
    onEachFeature: addHandlers
  }).addTo(map)

  // Liberal copying from http://leafletjs.com/examples/choropleth/
  infoBox = L.control()
  infoBox.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'infobox') // create a div with a class "info"
    this.update()
    return this._div
  }
  infoBox.update = function (nghdName, valueType) {
    if (nghdName) {
      this._div.innerHTML = '<h4>' + nghdName + '</h4>'
      if (valueType && valueType !== 'Neighborhood Bounds') {
        var displayValueType = valueType
        if (valueType.indexOf('Venues') >= 0 || valueType === 'Shops') {
          displayValueType += ' (per square mile)'
        } else if (valueType.indexOf('Crime') >= 0) {
          displayValueType += ' (per 1000 residents)'
        }
        this._div.innerHTML += ('<br>' + displayValueType + ': ' + Math.round(getValue(nghdName, valueType)))
      }
    } else {
      this._div.innerHTML = '<h4>Select a neighborhood</h4>'
    }
  }
  infoBox.addTo(map)
}

// Not the official centers, just ones that look good.
// TODO pull these out to the store.js
var cityCenters = {
  'Pittsburgh': [40.441, -79.97],
  'San Francisco': [37.77, -122.416],
  'Chicago': [41.876, -87.625],
  'Houston': [29.75, -95.371],
  'Austin': [30.268, -97.743]
}
var cityBounds = {
  'Pittsburgh': [[40.37, -80.13], [40.51, -79.82]],
  'San Francisco': [[37.68, -122.55], [37.82, -122.35]],
  'Chicago': [[41.6, -87.8], [42.20, -87.5]],
  'Houston': [[29.4, -95.5], [30.1, -95.2]],
  'Austin': [[30.1, -98.0], [30.5, -97.5]]
}
var zoomLevel = 12 // Starting zoom when you move to a new city.

// Need to make this a function instead of just a map b/c apparently you can't
// require() an expression that's not a literal string?
// TODO pull these out to the store.js
function getGeojsonForCity (city) {
  if (city === 'Pittsburgh') {
    return require('assets/pgh/nghd_bounds.geojson')
  } else if (city === 'San Francisco') {
    return require('assets/sf/nghd_bounds.geojson')
  } else if (city === 'Chicago') {
    return require('assets/chicago/nghd_bounds.geojson')
  } else if (city === 'Houston') {
    return require('assets/houston/nghd_bounds.geojson')
  } else if (city === 'Austin') {
    return require('assets/austin/nghd_bounds.geojson')
  }
}

// Map a walkscore from a number to a color
var walkscoreColor = function (num) {
  if (num < 30) {
    return '#f7fcf5'
  } else if (num < 40) {
    return '#e5f5e0'
  } else if (num < 50) {
    return '#c7e9c0'
  } else if (num < 60) {
    return '#a1d99b'
  } else if (num < 70) {
    return '#74c476'
  } else if (num < 80) {
    return '#41ab5d'
  } else if (num < 90) {
    return '#238b45'
  } else if (num <= 100) {
    return '#005a32'
  } else {
    return '#999999' // This shouldn't happen.
  }
}
// TODO adjust this scale
var crimesColor = function (num) {
  if (num < 25) {
    return '#ffffcc'
  } else if (num < 50) {
    return '#ffeda0'
  } else if (num < 75) {
    return '#fed976'
  } else if (num < 100) {
    return '#feb24c'
  } else if (num < 125) {
    return '#fd8d3c'
  } else if (num < 150) {
    return '#fc4e2a'
  } else if (num < 175) {
    return '#e31a1c'
  } else {
    return '#b10026'
  }
}
var venuesColor = function (num) {
  if (num < 5) {
    return '#fff7fb'
  } else if (num < 10) {
    return '#ece7f2'
  } else if (num < 20) {
    return '#d0d1e6'
  } else if (num < 40) {
    return '#a6bddb'
  } else if (num < 80) {
    return '#74a9cf'
  } else if (num < 160) {
    return '#3690c0'
  } else if (num < 320) {
    return '#0570b0'
  } else {
    return '#034e7b'
  }
}

// e.g. neighborhood = 'Shadyside' and valueType = 'Walk Score' and it would return 95.
function getValue (nghdName, valueType) {
  if (['Walk Score', 'Bike Score', 'Transit Score'].indexOf(valueType) >= 0) {
    var allWalkscores = store.state.neighborhoodsWalkscores[store.state.currentCity]
    for (var i = 0; i < allWalkscores.length; i++) {
      if (allWalkscores[i]['Name'] === nghdName) {
        return allWalkscores[i][valueType]
      }
    }
  } else if (['Total Crime', 'Part 1 Crime', 'Part 2 Crime'].indexOf(valueType) >= 0) {
    var allCrimes = store.state.neighborhoodsCrimeStats[store.state.currentCity]
    for (var j = 0; j < allCrimes.length; j++) {
      if (allCrimes[j]['neighborhood'] === nghdName) {
        if (valueType === 'Total Crime') {
          return parseFloat(allCrimes[j]['total_per_1000_ppl']) / 2
          // Divide by 2 b/c there's going to be twice as much "all crime" as
          // any subtype of crime.
        } else if (valueType === 'Part 1 Crime') {
          return parseFloat(allCrimes[j]['part1_per_1000_ppl'])
        } else if (valueType === 'Part 2 Crime') {
          return parseFloat(allCrimes[j]['part2_per_1000_ppl'])
        }
      }
    }
  } else if (valueType.indexOf('Venues') >= 0 || valueType === 'Shops') {
    var allVenues = store.state.neighborhoodsFoursquareVenues[store.state.currentCity]
    for (var k = 0; k < allVenues.length; k++) {
      if (allVenues[k]['Neighborhood'] === nghdName) {
        if (valueType === 'Arts Venues') {
          return parseFloat(allVenues[k]['Arts and Entertainment'])
        } else if (valueType === 'Nightlife Venues') {
          return parseFloat(allVenues[k]['Nightlife Spot'])
        } else if (valueType === 'Shops') {
          return parseFloat(allVenues[k]['Shop & Service'])
        } else if (valueType === 'Outdoor and Recreation Venues') {
          return parseFloat(allVenues[k]['Outdoors & Recreation'])
        } else if (valueType === 'Food Venues') {
          return parseFloat(allVenues[k]['Food'])
        } else if (valueType === 'All Venues') {
          return parseFloat(allVenues[k]['All Venues'])
        }
      }
    }
  }
}

function getColor (feature) {
  var nghdName = feature['properties']['name']
  var score = getValue(nghdName, store.state.currentMap)
  if (['Walk Score', 'Bike Score', 'Transit Score'].indexOf(store.state.currentMap) >= 0) {
    return walkscoreColor(score)
  } else if (['Part 1 Crime', 'Part 2 Crime'].indexOf(store.state.currentMap) >= 0) {
    return crimesColor(score)
  } else if (store.state.currentMap === 'Total Crime') {
    return crimesColor(score / 2.0) // because this includes 2 kinds of crime.
  } else if (store.state.currentMap === 'All Venues') {
    return venuesColor(score / 5.0)
  } else if (store.state.currentMap.indexOf('Venues') >= 0 || store.state.currentMap === 'Shops') {
    return venuesColor(score)
  } else {
    return '#333' // This shouldn't happen.
  }
}
function geojsonStyle (feature) {
  return {
    color: getColor(feature)
  }
}

export default {
  data () {
    return {
      store: store
    }
  },
  watch: {
    // When |currentCity| changes, do something.
    currentCity: function (newCity) {
      var newCityCenter = cityCenters[newCity]
      if (newCity === 'Houston') {
        zoomLevel = 11 // Houston is big.
      } else {
        zoomLevel = 12
      }
      map.setMaxBounds(cityBounds[newCity])
      map.setView(newCityCenter, zoomLevel)

      // Put the new city's neighborhoods on the map.
      geojsonLayer.removeFrom(map)
      var neighborhoodsGeojson = getGeojsonForCity(newCity)
      geojsonLayer = L.geoJSON(neighborhoodsGeojson, {
        style: geojsonStyle,
        onEachFeature: addHandlers
      }).addTo(map)
    },
    currentNghd: function (newNghd) {
      if (newNghd in mapFeatures) {
        doHighlight(mapFeatures[newNghd])
      }
    },
    currentMap: function () {
      geojsonLayer.setStyle(geojsonStyle)
    }
  },
  computed: {
    currentCity: function () { return store.state.currentCity },
    currentNghd: function () { return store.state.currentNeighborhood },
    currentMap: function () { return store.state.currentMap }
  },
  methods: {
    setCurrentMap
  },
  mounted: function () {
    this.$nextTick(function () {
      let nghdsGeojson = getGeojsonForCity(store.state.currentCity)
      setUpMap(cityCenters[store.state.currentCity], nghdsGeojson)
      map.setMaxBounds(cityBounds[store.state.currentCity])
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.city-map {
  text-align: center
}
#leafletMap {
  height: 360px;
}
</style>
<style>
.infobox {
    width: 250px;
    padding: 6px 2px;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
}
.infobox h4 {
    margin: 0;
    color: #777;
}
.map_picker {
  font-size:14pt;
}
</style>

