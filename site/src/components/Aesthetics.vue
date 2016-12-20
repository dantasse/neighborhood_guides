<template>
  <div class="aesthetics">
    <h3>What do people take photos of in {{store.state.currentNeighborhood}}</h3>
    Indoor photos: {{indoor_outdoor[0]}}, outdoor photos: {{indoor_outdoor[1]}}
    <div v-on:click="should_display=!should_display" id="toggle_link">
      <a v-show="should_display">Hide photos</a>
      <a v-show="!should_display">Show photos</a>
    </div>
    <table>
      <tr v-for='tag in top10tags'>
        <td class="autotag_name">
          <span v-if="tag['autotag']=='blackandwhite'">black and white</span>
          <span v-else>{{tag['autotag']}}</span>
        </td>
        <td v-if="should_display">
          <span v-for="i in [0,1,2,3,4]">
            <a v-if="i<tag['example_url'].length" v-bind:href="tag['example_url'][i]">
              <img v-bind:src="tag['example_url'][i]" class='preview_photo'/>
            </a>
          </span>
        </td>
      </tr>
    </table>
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
      should_display: true
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

