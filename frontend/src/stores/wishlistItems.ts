import { defineStore } from 'pinia';
import { WishlistItem } from '../types';

// restaurants Store
export const useWishlistItemsStore = defineStore('wishlistItems', {
    state: (): {wishlistItems: WishlistItem[]} => ({
        wishlistItems: [] as WishlistItem[], // Holds an array of wishlistItems
    }),
    getters: {
        // Example getter: find a restaurant by ID
        getWishlistItemById: (state) => (id: number) => {
            return state.wishlistItems.find(wishlistItem => wishlistItem.id === id);
        },
        getWishlistItemByName: (state) => (name: string) => {
            return state.wishlistItems.find(wishlistItem => wishlistItem.wishlistItem === name);
        },
    },
    actions: {
        // Save the list of hobbies
        saveWishlistItems(wishlistItems: WishlistItem[]) {
            this.wishlistItems = wishlistItems
        },

        // Add a new restaurant
        addWishlistItem(wishlistItem: WishlistItem) {
            this.wishlistItems.push(wishlistItem);
        },

        // Remove a restaurant by ID
        removeWishlistItem(id: number) {
            this.wishlistItems = this.wishlistItems.filter(wishlistItem => wishlistItem.id !== id);
        },
    },
});