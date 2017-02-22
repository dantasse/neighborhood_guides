import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// TODO not sure how to load this asychronously.
let pghNeighborhoodsAutotags = require('../assets/pgh/nghd_autotags.json')
let sfNeighborhoodsAutotags = require('../assets/sf/nghd_autotags.json')
let chiNeighborhoodsAutotags = require('../assets/chicago/nghd_autotags.json')
let houNeighborhoodsAutotags = require('../assets/houston/nghd_autotags.json')
let ausNeighborhoodsAutotags = require('../assets/austin/nghd_autotags.json')

let pghCrimeStats = require('../assets/pgh/crimes.csv')
let sfCrimeStats = require('../assets/sf/crimes.csv')
let chiCrimeStats = require('../assets/chicago/crimes.csv')
let houCrimeStats = require('../assets/houston/crimes.csv')
let ausCrimeStats = require('../assets/austin/crimes.csv')

let pghNghdsWalkscores = require('../assets/pgh/nghd_walkscores.csv')
let sfNghdsWalkscores = require('../assets/sf/nghd_walkscores.csv')
let chiNghdsWalkscores = require('../assets/chicago/nghd_walkscores.csv')
let houNghdsWalkscores = require('../assets/houston/nghd_walkscores.csv')
let ausNghdsWalkscores = require('../assets/austin/nghd_walkscores.csv')

let pghTop10TweetTfidf = require('../assets/pgh/tweet_tfidf_top10.json')
let sfTop10TweetTfidf = require('../assets/sf/tweet_tfidf_top10.json')
let chiTop10TweetTfidf = require('../assets/chicago/tweet_tfidf_top10.json')
let houTop10TweetTfidf = require('../assets/houston/tweet_tfidf_top10.json')
let ausTop10TweetTfidf = require('../assets/austin/tweet_tfidf_top10.json')

let pghFoursquareVenues = require('../assets/pgh/nghd_4sq.csv')
let sfFoursquareVenues = require('../assets/sf/nghd_4sq.csv')
let chiFoursquareVenues = require('../assets/chicago/nghd_4sq.csv')
let houFoursquareVenues = require('../assets/houston/nghd_4sq.csv')
let ausFoursquareVenues = require('../assets/austin/nghd_4sq.csv')

let pghMapillaryPhotos = require('../assets/pgh/nghd_mapillary_keys.csv')
let sfMapillaryPhotos = require('../assets/sf/nghd_mapillary_keys.csv')
let chiMapillaryPhotos = require('../assets/chicago/nghd_mapillary_keys.csv')
let houMapillaryPhotos = require('../assets/houston/nghd_mapillary_keys.csv')
let ausMapillaryPhotos = require('../assets/austin/nghd_mapillary_keys.csv')

let pghSfComparisons = require('../assets/pgh_sf_comparisons.json')
let pghHouComparisons = require('../assets/pgh_houston_comparisons.json')
let pghChiComparisons = require('../assets/pgh_chicago_comparisons.json')
let pghAusComparisons = require('../assets/pgh_austin_comparisons.json')
let sfHouComparisons = require('../assets/sf_houston_comparisons.json')
let sfPghComparisons = require('../assets/sf_pgh_comparisons.json')
let sfChiComparisons = require('../assets/sf_chicago_comparisons.json')
let sfAusComparisons = require('../assets/sf_austin_comparisons.json')
let houPghComparisons = require('../assets/houston_pgh_comparisons.json')
let houSfComparisons = require('../assets/houston_sf_comparisons.json')
let houChiComparisons = require('../assets/houston_chicago_comparisons.json')
let houAusComparisons = require('../assets/houston_austin_comparisons.json')
let chiPghComparisons = require('../assets/chicago_pgh_comparisons.json')
let chiSfComparisons = require('../assets/chicago_sf_comparisons.json')
let chiHouComparisons = require('../assets/chicago_houston_comparisons.json')
let chiAusComparisons = require('../assets/chicago_austin_comparisons.json')
let ausPghComparisons = require('../assets/austin_pgh_comparisons.json')
let ausSfComparisons = require('../assets/austin_sf_comparisons.json')
let ausHouComparisons = require('../assets/austin_houston_comparisons.json')
let ausChiComparisons = require('../assets/austin_chicago_comparisons.json')

let pghBounds = require('../assets/pgh/nghd_bounds.geojson')
let sfBounds = require('../assets/sf/nghd_bounds.geojson')
let chiBounds = require('../assets/chicago/nghd_bounds.geojson')
let houBounds = require('../assets/houston/nghd_bounds.geojson')
let ausBounds = require('../assets/austin/nghd_bounds.geojson')

let nghdNames = {'Pittsburgh': [], 'San Francisco': [], 'Chicago': [], 'Houston': [], 'Austin': []}
for (let nghd of pghBounds['features']) {
  nghdNames['Pittsburgh'].push(nghd['properties']['name'])
}
for (let nghd of sfBounds['features']) {
  nghdNames['San Francisco'].push(nghd['properties']['name'])
}
for (let nghd of chiBounds['features']) {
  nghdNames['Chicago'].push(nghd['properties']['name'])
}
for (let nghd of houBounds['features']) {
  nghdNames['Houston'].push(nghd['properties']['name'])
}
for (let nghd of ausBounds['features']) {
  let nghdName = nghd['properties']['name']
  if (nghdNames['Austin'].indexOf(nghdName) < 0) {
    nghdNames['Austin'].push(nghd['properties']['name'])
  }
}
export default new Vuex.Store({
  state: {
    cityList: ['Pittsburgh', 'San Francisco', 'Chicago', 'Houston', 'Austin'],
    currentNeighborhood: 'Shadyside',
    currentCity: 'Pittsburgh',
    compareNeighborhood: 'Mission',
    compareCity: 'San Francisco',
    neighborhoodNames: nghdNames,
    neighborhoodsAutotags: {'Pittsburgh': pghNeighborhoodsAutotags, 'San Francisco': sfNeighborhoodsAutotags, 'Chicago': chiNeighborhoodsAutotags, 'Houston': houNeighborhoodsAutotags, 'Austin': ausNeighborhoodsAutotags},
    neighborhoodsCrimeStats: {'Pittsburgh': pghCrimeStats, 'San Francisco': sfCrimeStats, 'Chicago': chiCrimeStats, 'Houston': houCrimeStats, 'Austin': ausCrimeStats},
    neighborhoodsWalkscores: {'Pittsburgh': pghNghdsWalkscores, 'San Francisco': sfNghdsWalkscores, 'Chicago': chiNghdsWalkscores, 'Houston': houNghdsWalkscores, 'Austin': ausNghdsWalkscores},
    neighborhoodsTop10TweetTfidf: {'Pittsburgh': pghTop10TweetTfidf, 'San Francisco': sfTop10TweetTfidf, 'Chicago': chiTop10TweetTfidf, 'Houston': houTop10TweetTfidf, 'Austin': ausTop10TweetTfidf},
    neighborhoodsFoursquareVenues: {'Pittsburgh': pghFoursquareVenues, 'San Francisco': sfFoursquareVenues, 'Chicago': chiFoursquareVenues, 'Houston': houFoursquareVenues, 'Austin': ausFoursquareVenues},
    neighborhoodsMapillaryPhotos: {'Pittsburgh': pghMapillaryPhotos, 'San Francisco': sfMapillaryPhotos, 'Chicago': chiMapillaryPhotos, 'Houston': houMapillaryPhotos, 'Austin': ausMapillaryPhotos},
    comparisons: {
      'Pittsburgh': {
        'San Francisco': pghSfComparisons,
        'Houston': pghHouComparisons,
        'Chicago': pghChiComparisons,
        'Austin': pghAusComparisons
      },
      'San Francisco': {
        'Pittsburgh': sfPghComparisons,
        'Houston': sfHouComparisons,
        'Chicago': sfChiComparisons,
        'Austin': sfAusComparisons
      },
      'Houston': {
        'Pittsburgh': houPghComparisons,
        'San Francisco': houSfComparisons,
        'Chicago': houChiComparisons,
        'Austin': houAusComparisons
      },
      'Chicago': {
        'Pittsburgh': chiPghComparisons,
        'San Francisco': chiSfComparisons,
        'Houston': chiHouComparisons,
        'Austin': chiAusComparisons
      },
      'Austin': {
        'Pittsburgh': ausPghComparisons,
        'San Francisco': ausSfComparisons,
        'Houston': ausHouComparisons,
        'Chicago': ausChiComparisons
      }
    }
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
      let alltags = state.neighborhoodsAutotags[state.currentCity][state.currentNeighborhood]
      if (alltags === undefined) {
        return []
      } else {
        return alltags['autotags_90plus_minusbaseline']
      }
    },
    indoor_outdoor: function (state) {
      let alltags = state.neighborhoodsAutotags[state.currentCity][state.currentNeighborhood]
      if (alltags === undefined) {
        return [0, 0]
      } else {
        return [alltags['num_indoor'], alltags['num_outdoor']]
      }
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
      return state.neighborhoodsTop10TweetTfidf[state.currentCity][state.currentNeighborhood]
    },
    foursquareVenues: function (state) {
      for (let nghd of state.neighborhoodsFoursquareVenues[state.currentCity]) {
        if (nghd['Neighborhood'] === state.currentNeighborhood) {
          var currentNghd = nghd
        } else if (nghd['Neighborhood'] === state.currentCity) {
          var currentCity = nghd
        }
      }
      for (let nghd of state.neighborhoodsFoursquareVenues[state.compareCity]) {
        if (nghd['Neighborhood'] === state.compareNeighborhood) {
          var compareNghd = nghd
        } else if (nghd['Neighborhood'] === state.compareCity) {
          var compareCity = nghd
        }
      }
      return {'currentNghd': currentNghd,
        'currentCity': currentCity,
        'compareNghd': compareNghd,
        'compareCity': compareCity
      }
    },
    mapillaryPhotos: function (state) {
      console.log('here')
      console.log(state.neighborhoodsMapillaryPhotos['Pittsburgh'])
      for (let nghd of state.neighborhoodsMapillaryPhotos[state.currentCity]) {
        if (nghd['neighborhood'] === state.currentNeighborhood) {
          console.log('match')
          console.log(nghd['neighborhood'])
          var currentNghd = nghd
        }
      }
      for (let nghd of state.neighborhoodsMapillaryPhotos[state.compareCity]) {
        if (nghd['neighborhood'] === state.compareNeighborhood) {
          var compareNghd = nghd
        }
      }
      console.log({'currentNghd': currentNghd, 'compareNghd': compareNghd})

      return {'currentNghd': currentNghd, 'compareNghd': compareNghd}
    },
    comparisons: function (state) {
      return state.comparisons[state.compareCity][state.currentCity]
    }
  }
})

