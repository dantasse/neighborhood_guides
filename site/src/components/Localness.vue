<template>
  <div class="localness">
    <h3>What do people talk about in {{store.state.currentNeighborhood}}</h3>
    <ul>
      {{top10TweetTfidf}}
    </ul>
    <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
import { mapGetters } from 'vuex'

export default {
  computed: mapGetters([
    'top10TweetTfidf'
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


