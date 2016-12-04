<template>
  <div class="aesthetics">
    <h3>What do people take photos of in {{store.state.currentNeighborhood}}</h3>
    Indoor photos: {{indoor_outdoor[0]}}, outdoor photos: {{indoor_outdoor[1]}}
    <ul>
      <li v-for='tag in top10tags' v-on:click="should_display=!should_display">
        {{tag['autotag']}}
        <div v-if="should_display">
          <span v-for="i in [0,1,2]">
            <img v-bind:src="tag['example_url'][i]" class='preview_photo'/>
          </span>
        </div>
      </li>
    </ul>
    <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'top10tags',
    'indoor_outdoor'
  ]),
  // mapGetters is syntactic sugar; could also say:
  // computed: {
  //   top10tags () {
  //     return store.getters.top10tags
  //   }
  // },
  data () {
    return {
      store: store,
      should_display: false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.preview_photo {
  width: 200px;
  height: 150px;
}
</style>

