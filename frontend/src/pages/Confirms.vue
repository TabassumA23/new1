<template>
  <main class="reservations-page">
    <div class="card reservation-card">
      <h2>Reservations</h2>

      <div
        class="reservation-item"
        v-for="(reservation, index) in paginatedReservations"
        :key="reservation.id"
      >
        <div class="reservation-header">
          <h3>Restaurant: {{ reservation.restaurant.name }}</h3>
          <p><strong>By:</strong> {{ reservation.user.first_name }} {{ reservation.user.last_name }}</p>
        </div>

        <div class="reservation-content">
          <p><strong>Time:</strong> {{ reservation.reservation_time }}</p>
          <p><strong>Guests:</strong> {{ reservation.number_of_people }}</p>
          <p><strong>Special Requests:</strong> {{ reservation.special_requests }}</p>
        </div>

        <div
          class="reservation-content"
          v-if="getRestaurantOwnerId(reservation.restaurant.id) === user.id"
        >
          <p><strong>Status:</strong></p>
          <select v-model="reservation.status" @change="updateStatus(reservation)">
            <option value="0">Pending</option>
            <option value="1">Confirmed</option>
          </select>
        </div>

        <div
          class="reservation-actions"
          v-if="reservation.user.id === user.id"
        >
          <button @click="deleteReservation(reservation.id)">Delete Reservation</button>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/user";
import { useReservationsStore } from "../stores/reservations";
import { Reservation, Restaurant, User } from "../types";
import VueCookies from "vue-cookies";

export default defineComponent({
  data() {
    return {
      currentPage: 1,
      perPage: 5,
    };
  },
  computed: {
    user(): User {
      const userStore = useUserStore();
      return userStore.user;
    },
    reservations(): Reservation[] {
      const reservationsStore = useReservationsStore();
      return reservationsStore.reservations;
    },
    totalPages(): number {
      return Math.ceil(this.reservations.length / this.perPage);
    },
    paginatedReservations(): Reservation[] {
      const start = (this.currentPage - 1) * this.perPage;
      return this.reservations.slice(start, start + this.perPage);
    },
  },
  methods: {
    getRestaurantOwnerId(restaurantId: number) {
      // Assuming you have restaurant store logic elsewhere
      return null;
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    async deleteReservation(reservationId: number) {
      try {
        const response = await fetch(`http://localhost:8000/reservation/${reservationId}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
        });

        if (response.ok) {
          window.location.reload();
          alert("Reservation deleted successfully!");
        } else {
          alert("Failed to delete reservation.");
        }
      } catch (error) {
        console.error("Error deleting reservation:", error);
        alert("Error occurred while deleting reservation.");
      }
    },
    async updateStatus(reservation: Reservation) {
      try {
        const payload = {
          status: reservation.status,
        };

        const response = await fetch(`http://localhost:8000/reservation/${reservation.id}/`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${VueCookies.get("access_token")}`,
            "Content-Type": "application/json",
            "X-CSRFToken": VueCookies.get("csrftoken"),
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          window.location.reload();
          alert("Status updated successfully!");
        } else {
          alert("Failed to update reservation status.");
        }
      } catch (error) {
        console.error("Error updating reservation status:", error);
        alert("Error occurred while updating reservation status.");
      }
    },
  },
});
</script>

<style scoped>
:root {
  --bg-start: #0f0c29;
  --bg-end: #302b63;
  --card-bg: rgba(255, 255, 255, 0.05);
  --accent: #ff00c1;
  --text: #eee;
  --muted: #aaa;
  --radius: 12px;
}

.reservations-page {
  background: linear-gradient(135deg, var(--bg-start), var(--bg-end));
  min-height: 100vh;
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
  color: var(--text);
}

.card.reservation-card {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: var(--radius);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.reservations-page h2 {
  margin-bottom: 1rem;
}

.reservation-item {
  background: var(--card-bg);
  margin: 1rem 0;
  padding: 1rem;
  border-radius: var(--radius);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.reservation-header h3 {
  margin: 0 0 0.5rem;
  color: var(--accent);
  font-size: 1.4rem;
}

.reservation-header p {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.reservation-content p {
  margin: 0.5rem 0;
  color: var(--text);
}

select {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #ff8c00;
  border-radius: 10px;
  padding: 0.5rem;
  color: #000;
  margin-top: 0.25rem;
  font-size: 1rem;
}

select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255, 0, 193, 0.2);
}

.reservation-actions {
  text-align: right;
  margin-top: 1rem;
}

.reservation-actions button {
  background: linear-gradient(90deg, #ff0080, #ff8c00);
  border: none;
  padding: 0.5rem 1rem;
  color: #fff;
  font-weight: 600;
  border-radius: var(--radius);
  cursor: pointer;
  transition: transform 0.15s ease, opacity 0.2s;
}

.reservation-actions button:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.pagination-controls button {
  background: linear-gradient(90deg, #ff0080, #ff8c00);
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
