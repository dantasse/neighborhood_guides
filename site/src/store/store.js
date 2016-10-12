import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let neighborhoodsAutotags = require('../assets/pgh_nghd_autotags.json')
// TODO not sure how to load this asychronously.

export default new Vuex.Store({
  state: {
    currentNeighborhood: 'Shadyside',
    neighborhoodNames: Object.keys(neighborhoodsAutotags),
    neighborhoodsAutotags: neighborhoodsAutotags
  },
  mutations: {
    // To call this, call e.g. store.commit('selectNeighborhood', 'Shadyside')
    selectNeighborhood: function (state, newNghd) {
      state.currentNeighborhood = newNghd
    }
  },
  actions: {
    selectNeighborhood ({ commit }, newNghd) {
      commit('selectNeighborhood', newNghd)
      // This seems dumb here, this action just redirects to the mutation, but
      // I think it will make sense when we have bigger actions.
    }
  },
  getters: {
    top10tags: function (state) {
      let alltags = state.neighborhoodsAutotags[state.currentNeighborhood]['autotags_90plus_minusbaseline']
      let sortable = []
      Object.keys(alltags).forEach(function (key) {
        sortable.push([key, alltags[key]])
      })
      sortable.sort(function (x, y) {
        return y[1] - x[1]
      })
      return sortable.slice(0, 10)
    }
  }
})

