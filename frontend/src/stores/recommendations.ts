// import { defineStore } from 'pinia'
// import { Restaurant } from '../types';

// export const useRecommendationsStore = defineStore('recommendations', {
//   state: () => ({
//     restaurants: [] as Restaurant[],
//   }),
//   actions: {
//     set(newList: Restaurant[]) {
//       this.restaurants = newList
//     }
//   }
// })
// stores/recommendations.ts
import { defineStore } from 'pinia'
import type { Recommendation } from '../types'

export const useRecommendationsStore = defineStore('recommendations', {
  state: () => ({
    list: [] as Recommendation[],
  }),
  getters: {
    byId: (state) => (id: number) => state.list.find(r => r.id === id),
    // any other filters you need…
  },
  actions: {
    setAll(recs: Recommendation[]) {
      this.list = recs
    },
    add(rec: Recommendation) {
      this.list.push(rec)
    },
    remove(id: number) {
      this.list = this.list.filter(r => r.id !== id)
    },
    async fetchForCurrentUser(userId: number) {
      const res = await fetch(`/api/users/${userId}/recommendations`)
      const data = await res.json()
      this.setAll(data.recommendations)
    }
  }
})
