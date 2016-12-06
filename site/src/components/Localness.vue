<template>
  <div class="localness">
    <h3>What do people talk about in {{store.state.currentNeighborhood}}</h3>
    Click for context.
    <ul>
      <li v-for="tweetword in top10TweetTfidf">
        <span v-on:click="expandTweetWord(tweetword['word'])" >{{tweetword['word']}}</span>
        <div v-show="expanded.indexOf(tweetword['word']) >= 0">
          <ul>
            <li v-for="sentence in tweetword['context']">
            {{sentence}}
            </li>
          </ul>
        </div>
      </li>
    </ul>
    <br/>
  </div>
</template>


<script>
import store from '../store/store.js'
// import { mapGetters } from 'vuex'

// Yes, we're managing state here, but it's all local. Plus I got into a big
// mess trying to manage it more globally.
let expanded = []
let expandTweetWord = function (word) {
  if (expanded.indexOf(word) >= 0) {
    expanded.splice(expanded.indexOf(word), 1)
  } else {
    expanded.push(word)
  }
}

export default {
  computed: {
    top10TweetTfidf: function () {
      return store.getters.top10TweetTfidf
    }
  },
  data () {
    return {
      store: store,
      expandTweetWord: expandTweetWord,
      expanded: expanded
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
span {
  cursor: pointer;
}
span:hover {
  color: #42b983;
}
</style>


