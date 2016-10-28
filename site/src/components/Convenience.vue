<template>
  <div class="convenience">
    <h3>Location convenience in {{store.state.currentNeighborhood}}</h3>
    <ul v-if="'Walk Score' in walkscores">
      <li>Walk Score: {{walkscores['Walk Score']}}</li>
      <li>Transit Score: {{walkscores['Transit Score']}}</li>
      <li>Bike Score: {{walkscores['Bike Score']}}</li>
    </ul>
    <div v-else>
      No data for {{store.state.currentNeighborhood}}
    </div>
     <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'walkscores'
  ]),
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



