import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let neighborhoodsAutotags = require('../assets/pgh/nghd_autotags.json')
// TODO not sure how to load this asychronously.
let crimeStats = require('../assets/pgh_2015_crime_review.csv')
let nghdsWalkscores = require('../assets/pgh_nghd_walkscores.csv')
let top10TweetTfidf = require('../assets/pgh/tweet_tfidf_top10.json')
let foursquareVenues = require('../assets/pgh/nghd_4sq.csv')

export default new Vuex.Store({
  state: {
    currentNeighborhood: 'Shadyside',
    neighborhoodNames: Object.keys(neighborhoodsAutotags),
    neighborhoodsAutotags: neighborhoodsAutotags,
    neighborhoodsCrimeStats: crimeStats,
    neighborhoodsWalkscores: nghdsWalkscores,
    neighborhoodsTop10TweetTfidf: top10TweetTfidf,
    neighborhoodsFoursquareVenues: foursquareVenues
  },
  mutations: {
    // To call this, call e.g. store.commit('selectNeighborhood', 'Shadyside')
    // Mutations are synchronous.
    selectNeighborhood: function (state, newNghd) {
      state.currentNeighborhood = newNghd
    }
  },
  actions: {
    // To call this, call e.g. store.dispatch('selectNeighborhood', 'Shadyside')
    // Actions can be async.
    selectNeighborhood ({ commit }, newNghd) {
      commit('selectNeighborhood', newNghd)
      // This seems dumb here, this action just redirects to the mutation, but
      // I think it will make sense when we have bigger actions.
    }
  },
  getters: {
    top10tags: function (state) {
      let alltags = state.neighborhoodsAutotags[state.currentNeighborhood]['autotags_90plus_minusbaseline']
      // Get the top 10 for each neighborhood.
      // TODO: push this into the data pipeline instead.
      let sortable = []
      Object.keys(alltags).forEach(function (key) {
        sortable.push([key, alltags[key]])
      })
      sortable.sort(function (x, y) {
        return y[1] - x[1]
      })
      return sortable.slice(0, 10)
    },
    indoor_outdoor: function (state) {
      let alltags = state.neighborhoodsAutotags[state.currentNeighborhood]
      return [alltags['num_indoor'], alltags['num_outdoor']]
    },
    crimeStats: function (state) {
      for (let nghd of state.neighborhoodsCrimeStats) {
        if (nghd['Neighborhoods'] === state.currentNeighborhood) {
          let pop = nghd['Population 2010']
          let nghdStats = {
            'Part1Per1000': (1000.0 * nghd['Part I crimes'] / pop).toFixed(2),
            'Part2Per1000': (1000.0 * nghd['Part II crimes'] / pop).toFixed(2),
            'TotalPer1000': nghd['Crimes Per 1000']
          }
          return nghdStats
        }
      }
      return {}
    },
    walkscores: function (state) {
      for (let nghd of state.neighborhoodsWalkscores) {
        if (nghd['Name'] === state.currentNeighborhood) {
          return nghd
        }
      }
      return {}
    },
    top10TweetTfidf: function (state) {
      return state.neighborhoodsTop10TweetTfidf[state.currentNeighborhood]
    },
    foursquareVenues: function (state) {
      for (let nghd of state.neighborhoodsFoursquareVenues) {
        if (nghd['Neighborhood'] === state.currentNeighborhood) {
          return nghd
        }
      }
      return {}
    }

  }
})

