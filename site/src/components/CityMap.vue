<template>
  <div class="city-map">
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
var mapPicker // Control to say whether we want to look at crime, walkscores, etc.

var map

var mapFeatures = {}

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
  infoBox.update(layer.feature.properties)
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
  // Tiles are Mapbox Streets v10
  // https://www.mapbox.com/studio/styles/mapbox/streets-v10/share/
  L.tileLayer('http://a.tiles.mapbox.com/v4/mapbox.light/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZGFudGFzc2UiLCJhIjoiWkpJVUNjSSJ9.EEaUQpuPDkOhI8rX4ihVDQ', {
    id: 'mapbox.satellite',
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
  infoBox.update = function (props) {
    if (props) {
      this._div.innerHTML = '<h4>' + props['name'] + '</h4>'
    } else {
      this._div.innerHTML = '<h4>Select a neighborhood</h4>'
    }
  }
  infoBox.addTo(map)

  mapPicker = L.control()
  mapPicker.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'map_picker')
    var types = ['Neighborhood Bounds', 'Total Crime', 'Part 1 Crime',
      'Part 2 Crime', 'Walk Score', 'Bike Score', 'Transit Score',
      'Arts Venues', 'Nightlife Venues', 'Shops',
      'Outdoor and Recreation Venues', 'Food Venues', 'All Venues']
    var mapPickerHtml = '<select id="map_picker">'
    for (var i = 0; i < types.length; i++) {
      mapPickerHtml += '<option>' + types[i] + '</option>'
    }
    mapPickerHtml += '</select>'
    this._div.innerHTML = mapPickerHtml
    this.update()
    return this._div
  }
  mapPicker.update = function () {
  }
  mapPicker.addTo(map)
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
  'Chicago': [[41.86, -87.8], [41.89, -87.5]],
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
var walkscoreColor = function (number) {
  if (number < 12) {
    return '#f7fcf5'
  } else if (number < 25) {
    return '#e5f5e0'
  } else if (number < 37) {
    return '#c7e9c0'
  } else if (number < 50) {
    return '#a1d99b'
  } else if (number < 62) {
    return '#74c476'
  } else if (number < 75) {
    return '#41ab5d'
  } else if (number < 87) {
    return '#238b45'
  } else if (number <= 100) {
    return '#005a32'
  } else {
    console.log('huh?')
    console.log(number)
  }
}

function getColor (feature) {
  var nghdName = feature['properties']['name']
  var allWalkscores = store.state.neighborhoodsWalkscores[store.state.currentCity]
  for (var i = 0; i < allWalkscores.length; i++) {
    if (allWalkscores[i]['Name'] === nghdName) {
      var walkscore = allWalkscores[i]['Walk Score']

      return walkscoreColor(walkscore)
    }
  }
  return '#333'
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
    }
  },
  computed: {
    currentCity: function () { return store.state.currentCity },
    currentNghd: function () { return store.state.currentNeighborhood }
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

