<template>
  <div class="liveliness">
    <h3>How lively is {{store.state.currentNeighborhood}}</h3>
    <ul>
      <!--<li v-for='tag in top10tags'>-->
      <!--  {{tag[0]}}-->
      <!--</li>-->
    </ul>
    <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
  ]),
  // mapGetters is syntactic sugar; could also say:
  // computed: {
  //   top10tags () {
  //     return store.getters.top10tags
  //   }
  // },
  data () {
    return {
      store: store
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

