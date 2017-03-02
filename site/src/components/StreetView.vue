<template>
  <div class="streetview" id="streetview">
    <h3>What does {{ store.state.currentNeighborhood }} look like?</h3>
      <span v-for="url in streetViewPhotos.slice(0, 20)">
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
    'streetViewPhotos'
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
.preview_photo {
  height: 120px;
}
#toggle_link {
  cursor: pointer;
}
.autotag_name {
  font-size:12pt;
  padding: 0 10px 0 0;
}
</style>

