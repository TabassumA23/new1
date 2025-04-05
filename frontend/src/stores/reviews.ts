import { defineStore } from 'pinia';
import { Review } from '../types';

// restaurants Store
export const useReviewsStore = defineStore('reviews', {
    state: (): {reviews: Review[]} => ({
        reviews: [] as Review[], // Holds an array of reviews
    }),
    getters: {
        // Example getter: find a restaurant by ID
        getReviewById: (state) => (id: number) => {
            return state.reviews.find(review => review.id === id);
        },
        getReviewByName: (state) => (name: string) => {
            return state.reviews.find(review => review.review === name);
        },
    },
    actions: {
        // Save the list of hobbies
        saveReviews(reviews: Review[]) {
            this.reviews = reviews
        },

        // Add a new restaurant
        addReview(review: Review) {
            this.reviews.push(review);
        },

        // Remove a restaurant by ID
        removeReview(id: number) {
            this.reviews = this.reviews.filter(review => review.id !== id);
        },
    },
});