import { defineStore } from 'pinia';
import { Reservation } from '../types';

// restaurants Store
export const useReservationsStore = defineStore('reservations', {
    state: (): {reservations: Reservation[]} => ({
        reservations: [] as Reservation[], // Holds an array of hobbiess
    }),
    getters: {
        // Example getter: find a reservation by ID
        getReservationById: (state) => (id: number) => {
            return state.reservations.find(reservation => reservation.id === id);
        },
        getReservationByName: (state) => (restaurant: string) => {
            return state.reservations.find(reservation => reservation.restaurant === restaurant);
        },
    },
    actions: {
        // Save the list of hobbies
        saveReservations(reservations: Reservation[]) {
            this.reservations = reservations
        },

        // Add a new restaurant
        addReservation(reservation: Reservation) {
            this.reservations.push(reservation);
        },

        // Remove a restaurant by ID
        removeReservation(id: number) {
            this.reservations = this.reservations.filter(reservation => reservation.id !== id);
        },
    },
});