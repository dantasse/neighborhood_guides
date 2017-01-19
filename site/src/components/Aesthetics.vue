<template>
  <div class="aesthetics">
    <h3>What do people take photos of in {{store.state.currentNeighborhood}}</h3>
    Photos are from Flickr; selected photos have tags that appear more often in {{store.state.currentNeighborhood}} than in other neighborhoods.<br>
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
    <div v-on:click="display_mapillary=!display_mapillary" id="toggle_link">
      <a v-show="display_mapillary">Hide street view</a>
      <a v-show="!display_mapillary">Show street view</a>
    </div>
    <div v-if="display_mapillary">
      <iframe width="640" height="480" v-bind:src='getMapillaryUrl()' frameborder="0"></iframe>
    </div>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

function getMapillaryUrl () {
  var keys = JSON.parse(store.getters.mapillaryPhotos['currentNghd']['photo_keys'])
  var photoId = keys[Math.floor(Math.random() * keys.length)]
  return 'https://embed-v1.mapillary.com/embed?version=1&filter=%5B%22all%22%5D&map_filter=%5B%22all%22%5D&image_key=' + photoId + '&client_id=a2QzaEVDN3FFWWFIaGVfNEFaZ19Edzo4ZGJiNzg5NGVjZjc0Nzk1&style=photo'
}
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
      should_display: true,
      display_mapillary: false,
      getMapillaryUrl: getMapillaryUrl
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

