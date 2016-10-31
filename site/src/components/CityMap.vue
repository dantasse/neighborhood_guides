<template>
  <div class="city-map">
    <div id='leafletMap'>
    </div>
  </div>
</template>


<script>
import store from '../store/store.js'
import L from 'leaflet'
import neighborhoodsGeojson from 'assets/pgh/neighborhoods.geojson'

// Define this here so we can reference it in setUpMap and resetHighlight.
var geojsonLayer
var infoBox

function addHandlers (feature, layer) {
  layer.on({
    click: selectNghd,
    mouseover: highlightFeature,
    mouseout: resetHighlight
  })
}

function selectNghd (e) {
  let nghd = e.target.feature.properties.hood
  store.dispatch('selectNeighborhood', nghd)
}

function highlightFeature (e) {
  var layer = e.target

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

function setUpMap () {
  this.$nextTick(function () { // happen when the DOM is ready.
    var map = L.map('leafletMap', {
      minZoom: 3,
      maxZoom: 18,
      inertia: false
    })
    map.setView([40.441, -79.97], 12)
    // Tiles are Mapbox Streets v10
    // https://www.mapbox.com/studio/styles/mapbox/streets-v10/share/
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGFudGFzc2UiLCJhIjoiWkpJVUNjSSJ9.EEaUQpuPDkOhI8rX4ihVDQ', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 18
    }).addTo(map)
    geojsonLayer = L.geoJSON(neighborhoodsGeojson, {
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
        this._div.innerHTML = '<h4>' + props['hood'] + '</h4>'
      } else {
        this._div.innerHTML = '<h4>Select a neighborhood</h4>'
      }
    }
    infoBox.addTo(map)
  })
}

export default {
  data () {
    return {
      store: store
    }
  },
  mounted: setUpMap
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
    margin: 0 0 5px;
    color: #777;
}
</style>

