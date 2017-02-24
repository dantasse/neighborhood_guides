<template>
  <div class="nghd-list">
    <!-- A component must have one top level element, in this case the div.-->
    <h4>Particularly, this neighborhood:
      <select v-model='currentNghd' v-on:change='selectName'>
        <option value="" disabled>Select a Neighborhood</option>
        <option v-for='nghd in nghdNames' :value='nghd'>{{nghd}}</option>
      </select>
    </h4>
    <p id='similarNghds'>
    Similar to {{compareNghd}}:
      <span class='compareNghdName' v-for='nghd in nghdComparisons'>
        <a class="selectNghdLink" v-on:click="selectNameText(nghd['name'])">
          {{nghd['name']}} {{nghd['average']}}%
        </a>
        <a class="whyLink" v-on:click="displayWhy(nghd['name'])">why?</a>
      </span>
    </p>
    <p id='whyExplainer' v-show="nghdExplainedName !== ''">
      Similarity between {{compareNghd}} and {{nghdExplainedName}}:
      <a class="hideLink" v-on:click="displayWhy('')">(hide)</a>
      <ul>
        <li>What people say on Twitter: {{nghdExplanation['twitter']}}%</li>
        <li>What people take photos of on Flickr: {{nghdExplanation['flickr']}}%</li>
        <li>Venues on Foursquare: {{nghdExplanation['foursquare']}}%</li>
        <li>Crime data: {{nghdExplanation['crime']}}%</li>
        <li>Walkscores: {{nghdExplanation['walkscore']}}%</li>
      </ul>
    </p>
  </div>
</template>


<script>
import store from '../store/store.js'

// Here we can use ES6 (ES2015) features, like 'let'.
let selectName = function (ev) {
  // This is used by the select box.
  var selectedNghd = ev.target.value
  // This is how you call a method on the store:
  this.nghdExplainedName = ''
  store.dispatch('selectNeighborhood', selectedNghd)
}
let selectNameText = function (text) {
  this.nghdExplainedName = ''
  // This is used by the "closest neighborhood" links.
  store.dispatch('selectNeighborhood', text)
}

export default {
  data () {
    return {
      store: store,
      nghdExplainedName: '',
      nghdExplanation: {}
    }
  },
  methods: {
    selectName,
    selectNameText,
    displayWhy: function (nghd) {
      if (this.nghdExplainedName === nghd) {
        this.nghdExplainedName = ''
        // Quirk for UI smoothness - if you click "why" twice in a row it will
        // just collapse again.
      } else {
        this.nghdExplainedName = nghd
        for (let i = 0; i < this.nghdComparisons.length; i++) {
          if (this.nghdComparisons[i]['name'] === nghd) {
            this.nghdExplanation = this.nghdComparisons[i]
          }
        }
      }
    }
  },
  computed: {
    nghdNames: function () {
      var nghdNames = store.state.neighborhoodNames[store.state.currentCity].slice()
      // slice() is so we have a copy, not editing the names.
      nghdNames = nghdNames.sort().filter(function (x) { return x !== 'None' })
      return nghdNames
    },
    // Computed properties are cached based on their dependencies.
    currentNghd: function () { return store.state.currentNeighborhood },
    compareNghd: function () { return store.state.compareNeighborhood },
    nghdComparisons: function () {
      let comparisons = store.getters.comparisons[store.state.compareNeighborhood]
      let retval = []
      for (let key in comparisons) {
        let stats = comparisons[key]
        retval.push({name: key,
          average: (100 - Math.round(stats['average'] * 100)),
          twitter: (100 - Math.round(stats['twitter'] * 100)),
          foursquare: (100 - Math.round(stats['4sq'] * 100)),
          walkscore: (100 - Math.round(stats['walkscore'] * 100)),
          crime: (100 - Math.round(stats['crime'] * 100)),
          flickr: (100 - Math.round(stats['flickr'] * 100))
        })
      }
      retval = retval.sort(function (x, y) { return y['average'] - x['average'] })
      return retval
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  cursor: pointer;
}
#similarNghds {
  font-size: 18px;
}
.compareNghdName {
  padding: 5px;
}
.whyLink {
  font-size: 12px;
}
#whyExplainer {
  
}
</style>
