<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
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
        <safety></safety>
        <convenience></convenience>
        <localness></localness>
        <liveliness></liveliness>
        <!--To get a better understanding of how this boilerplate works, check out-->
        <!--<a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>.-->
      </div>
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
import Aesthetics from './components/Aesthetics'
import Safety from './components/Safety'
import Convenience from './components/Convenience'
import Localness from './components/Localness'
import Liveliness from './components/Liveliness'
import store from './store/store.js'

export default {
  components: {
    CityPicker,
    CityMap,
    NghdList,
    ComparePicker,
    CompareCityPicker,
    Aesthetics,
    Safety,
    Convenience,
    Localness,
    Liveliness
  },
  data () {
    return {
      store: store
    }
  }
}

</script>

<style>
</style>
