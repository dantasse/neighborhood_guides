<template>
  <div class="instagram" id="instagram" style="display:none">
    <h3>Photos from {{ store.state.currentNeighborhood }}</h3>
      <span v-for="url in instagrams.slice(0, 20)">
        <a v-bind:href="url">
          <img v-bind:src="url" class='preview_photo'/>
        </a>
      </span>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'instagrams'
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
.preview_photo {
  height: 180px;
}
</style>

