<template>
  <div class="city-map">
    <div id='leafletMap'>
    </div>
  </div>
</template>


<script>
import store from '../store/store.js'
import L from 'leaflet'

export default {
  data () {
    return {
      store: store
    }
  },
  mounted: function () {
    this.$nextTick(function () {
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
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.city-map {
  text-align: center
}
#leafletMap { height: 360px; }
</style>

