<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
  <div id="outer-container">
    <!--outer-container so we can bleed to the edge (header, footer)-->
    <div id="app" class="container">
      <div class="row">
        <div class="col-md-12">
          <compare-city-picker></compare-city-picker>
          <compare-picker></compare-picker>
          <city-picker></city-picker>
          <nghd-list></nghd-list>
          <city-map></city-map>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <!-- These all match the "export default" components below.-->
          <aesthetics></aesthetics>
          <flickr2></flickr2>
          <flickr3></flickr3>
          <instagram></instagram>
          <street-view></street-view>
          <convenience></convenience>
          <liveliness></liveliness>
          <safety></safety>
          <localness></localness>
          <!--To get a better understanding of how this boilerplate works, check out-->
          <!--<a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>.-->
        </div>
      </div>
    </div>
    <page-footer></page-footer>
    <div>
      Toggle options:
      <a onclick="$('#similarNghds').toggle()">Similar Neighborhoods</a>
      <a onclick="$('#liveliness').toggle(); $('#safety').toggle(); $('#convenience').toggle(); ">Graphs</a>
      <a onclick="$('#localness').toggle()">Tweets</a>
      <a onclick="$('#streetview').toggle()">Street View</a>
      <a onclick="$('#aesthetics').toggle()">Photos</a>
      <a onclick="$('#flickr2').toggle()">Flickr 2</a>
      <a onclick="$('#flickr3').toggle()">Flickr 3</a>
      <a onclick="$('#instagram').toggle()">Instagram</a>
    </div>

  </div>
</template>

<script>
// Here are the "subcomponents" we're using:
import CityPicker from './components/CityPicker'
import CityMap from './components/CityMap'
import NghdList from './components/NghdList'
import ComparePicker from './components/ComparePicker'
import CompareCityPicker from './components/CompareCityPicker'
import StreetView from './components/StreetView'
import Aesthetics from './components/Aesthetics'
import Flickr2 from './components/Flickr2'
import Flickr3 from './components/Flickr3'
import Instagram from './components/Instagram'
import Safety from './components/Safety'
import Convenience from './components/Convenience'
import Localness from './components/Localness'
import Liveliness from './components/Liveliness'
import PageFooter from './components/PageFooter'
import store from './store/store.js'

export default {
  components: {
    CityPicker,
    CityMap,
    NghdList,
    ComparePicker,
    CompareCityPicker,
    StreetView,
    Aesthetics,
    Flickr2,
    Flickr3,
    Instagram,
    Safety,
    Convenience,
    Localness,
    Liveliness,
    PageFooter
  },
  data () {
    return {
      store: store
    }
  }
}

</script>

<style>
a {
  cursor: pointer;
}
</style>
