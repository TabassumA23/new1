import { defineStore } from 'pinia';
import { Wishlist } from '../types';

// restaurants Store
export const useWishlistsStore = defineStore('wishlists', {
    state: (): {wishlists: Wishlist[]} => ({
        wishlists: [] as Wishlist[], // Holds an array of wishlists
    }),
    getters: {
        // getter: find a restaurant by ID
        getWishlistById: (state) => (id: number) => {
            return state.wishlists.find(wishlist => wishlist.id === id);
        },
        getWishlistByName: (state) => (name: string) => {
            return state.wishlists.find(wishlist => wishlist.wishlist === name);
        },
    },
    actions: {
        // Save the list of wishlists
        saveWishlists(wishlists: Wishlist[]) {
            this.wishlists = wishlists
        },

        // Add a new wishlist
        addWishlist(wishlist: Wishlist) {
            this.wishlists.push(wishlist);
        },

        // Remove a wishlist by ID
        removeWishlist(id: number) {
            this.wishlists = this.wishlists.filter(wishlist => wishlist.id !== id);
        },
    },
});