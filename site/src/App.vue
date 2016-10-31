<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-md-12">
        <city-map>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <nghd-list></nghd-list>
      </div>
      <div class="col-md-6">
        <h1>{{store.state.currentNeighborhood}}</h1>
        <h3>Compared to <select><option value="TODO">TODO</option></select></h3>
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
import CityMap from './components/CityMap'
import NghdList from './components/NghdList'
import Aesthetics from './components/Aesthetics'
import Safety from './components/Safety'
import Convenience from './components/Convenience'
import Localness from './components/Localness'
import Liveliness from './components/Liveliness'
import store from './store/store.js'

export default {
  components: {
    CityMap,
    NghdList,
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
