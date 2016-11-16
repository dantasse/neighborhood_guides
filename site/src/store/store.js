import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

let neighborhoodsAutotags = require('../assets/pgh/nghd_autotags.json')
// TODO not sure how to load this asychronously.
let pghCrimeStats = require('../assets/pgh/crimes.csv')
let sfCrimeStats = require('../assets/sf/crimes.csv')
let pghNghdsWalkscores = require('../assets/pgh/nghd_walkscores.csv')
let sfNghdsWalkscores = require('../assets/sf/nghd_walkscores.csv')
let top10TweetTfidf = require('../assets/pgh/tweet_tfidf_top10.json')
let foursquareVenues = require('../assets/pgh/nghd_4sq.csv')

let pghBounds = require('../assets/pgh/nghd_bounds.geojson')
let sfBounds = require('../assets/sf/nghd_bounds.geojson')
let nghdNames = {'Pittsburgh': [], 'San Francisco': []}
for (let nghd of pghBounds['features']) {
  nghdNames['Pittsburgh'].push(nghd['properties']['name'])
}
for (let nghd of sfBounds['features']) {
  nghdNames['San Francisco'].push(nghd['properties']['name'])
}
console.log(nghdNames)
export default new Vuex.Store({
  state: {
    cityList: ['Pittsburgh', 'San Francisco'],
    currentNeighborhood: 'Shadyside',
    currentCity: 'Pittsburgh',
    compareNeighborhood: '',
    compareCity: 'San Francisco',
    neighborhoodNames: nghdNames,
    neighborhoodsAutotags: neighborhoodsAutotags,
    neighborhoodsCrimeStats: {'Pittsburgh': pghCrimeStats, 'San Francisco': sfCrimeStats},
    neighborhoodsWalkscores: {'Pittsburgh': pghNghdsWalkscores, 'San Francisco': sfNghdsWalkscores},
    neighborhoodsTop10TweetTfidf: top10TweetTfidf,
    neighborhoodsFoursquareVenues: foursquareVenues
  },
  mutations: {
    // To call this, call e.g. store.commit('selectNeighborhood', 'Shadyside')
    // Mutations are synchronous.
    selectNeighborhood: function (state, newNghd) {
      state.currentNeighborhood = newNghd
    },
    selectCurrentCity: function (state, newCurrentCity) {
      state.currentCity = newCurrentCity
    },
    selectCompareNghd: function (state, newCompareNghd) {
      state.compareNeighborhood = newCompareNghd
    },
    selectCompareCity: function (state, newCompareCity) {
      state.compareCity = newCompareCity
    }
  },
  actions: {
    // To call this, call e.g. store.dispatch('selectNeighborhood', 'Shadyside')
    // Actions can be async.
    selectNeighborhood ({ commit }, newNghd) {
      commit('selectNeighborhood', newNghd)
      // This seems dumb here, this action just redirects to the mutation, but
      // I think it will make sense when we have bigger actions.
    },
    selectCurrentCity ({ commit }, newCurrentCity) {
      commit('selectCurrentCity', newCurrentCity)
    },
    selectCompareNghd ({ commit }, newCompareNghd) {
      commit('selectCompareNghd', newCompareNghd)
    },
    selectCompareCity ({ commit }, newCompareCity) {
      commit('selectCompareCity', newCompareCity)
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
      // TODO: replace all these csv lookups with json lookups ideally.
      for (let nghd of state.neighborhoodsCrimeStats[state.currentCity]) {
        if (nghd['neighborhood'] === state.currentNeighborhood) {
          var currentNghd = nghd
        } else if (nghd['neighborhood'] === state.currentCity) {
          var currentCity = nghd
        }
      }
      for (let nghd of state.neighborhoodsCrimeStats[state.compareCity]) {
        if (nghd['neighborhood'] === state.compareNeighborhood) {
          var compareNghd = nghd
        } else if (nghd['neighborhood'] === state.compareCity) {
          var compareCity = nghd
        }
      }
      return {'currentNghd': currentNghd,
        'currentCity': currentCity,
        'compareNghd': compareNghd,
        'compareCity': compareCity}
    },
    cityCrimeStats: function (state) {
      for (let nghd of state.neighborhoodsCrimeStats) {
        if (nghd['neighborhood'] === state.currentCity) {
          return nghd
        }
      }
      return {}
    },
    walkscores: function (state) {
      for (let nghd of state.neighborhoodsWalkscores[state.currentCity]) {
        if (nghd['Name'] === state.currentNeighborhood) {
          var currentNghd = nghd
        } else if (nghd['Name'] === state.currentCity) {
          var currentCity = nghd
        }
      }
      for (let nghd of state.neighborhoodsWalkscores[state.compareCity]) {
        if (nghd['Name'] === state.compareNeighborhood) {
          var compareNghd = nghd
        } else if (nghd['Name'] === state.compareCity) {
          var compareCity = nghd
        }
      }
      return {'currentNghd': currentNghd,
        'currentCity': currentCity,
        'compareNghd': compareNghd,
        'compareCity': compareCity}
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
    },
    cityFoursquareVenues: function (state) {
      for (let nghd of state.neighborhoodsFoursquareVenues) {
        if (nghd['Neighborhood'] === state.currentCity) {
          return nghd
        }
      }
      return {}
    }
  }
})

