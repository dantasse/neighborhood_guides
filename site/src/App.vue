<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-md-6">
        <nghd-list></nghd-list>
      </div>
      <div class="col-md-6">
        <aesthetics></aesthetics>
          <p>
            <!--To get a better understanding of how this boilerplate works, check out-->
            <!--<a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>.-->
          </p>
      </div>
    </div>
  </div>
</template>

<script>
// Here are the "subcomponents" we're using:
import NghdList from './components/NghdList'
import Aesthetics from './components/Aesthetics'

export default {
  components: {
    NghdList,
    Aesthetics
  }
}

</script>

<style>
</style>
