<!-- This is a "single file component"; more info at:
    http://vuejs.org/guide/single-file-components.html-->

<template>
  <div id="app">
    <nghd-list></nghd-list>
    <aesthetics></aesthetics>
    <p>
      To get a better understanding of how this boilerplate works, check out
      <a href="http://vuejs-templates.github.io/webpack" target="_blank">its documentation</a>.
    </p>
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
html {
  height: 100%;
}

body {
  display: flex;
  align-items: left;
  justify-content: left;
  height: 100%;
}

#app {
  max-width: 600px;
  font-family: Source Sans Pro, Helvetica, sans-serif;
  text-align: center;
}

#app a {
  text-decoration: none;
}

.logo {
  width: 100px;
  height: 100px
}
</style>
