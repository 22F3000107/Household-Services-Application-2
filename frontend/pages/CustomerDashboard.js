
import store from "../utils/store.js";

export default {
    template: `
    <div class="container mt-5 pt-4">
        <h2 class="text-dark">Customer Dashboard</h2>
        <p class="text-muted">Manage your booked services.</p>

        <a href="/book-service" class="btn btn-success mb-3">Book a New Service</a>

        <!-- Search Bar -->
        <div class="mb-3">
            <input v-model="searchQuery" class="form-control" placeholder="Search services..">
            <button @click="searchServices" class="btn btn-primary mt-2">Search</button>
        </div>

        <p v-if="loading" class="text-info">Loading your services...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <!-- Available Services Section -->
        <h3>Available Services</h3>
        <table v-if="services.available.length > 0" class="table table-bordered">
            <thead class="thead-light">
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Base_price</th>
                    <th>Time_required</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services.available" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.name }}</td>
                    <td>{{ service.base_price }}</td>
                    <td>{{ service.time_required}}</td>
                    <td>
                        <button class="btn btn-success btn-sm" @click="bookService(service.id)">Book</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-if="services.available.length === 0 && !loading" class="text-muted">No available services found.</p>

        <!-- Booked Services Section -->
        <h3 class="mt-4">Booked Services</h3>
        <table v-if="services.booked.length > 0" class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services.booked" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.service_name }}</td>
                    <td>{{ service.status }}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" @click="cancelService(service.id)">Cancel</button>
                        <button class="btn btn-warning btn-sm" @click="closeService(service.id)">Close</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-if="services.booked.length === 0 && !loading" class="text-muted">No active bookings.</p>

        <!-- Closed Services Section -->
        <h3 class="mt-4">Closed Services</h3>
        <table v-if="services.closed.length > 0" class="table table-bordered">
            <thead class="thead-light">
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services.closed" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.service_name }}</td>
                    <td>{{ service.status }}</td>
                    <td>
                        <button class="btn btn-info btn-sm" @click="openReviewModal(service.id)">Leave Review</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-if="services.closed.length === 0 && !loading" class="text-muted">No closed services yet.</p>


        <!-- Review Modal -->
        <div v-if="showReviewModal" class="modal" style="display: block;">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Leave a Review</h5>
                        <button type="button" class="close" @click="closeReviewModal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <label>Rating (1-5):</label>
                        <select v-model="review.rating" class="form-control">
                            <option value="1">1 - Poor</option>
                            <option value="2">2 - Fair</option>
                            <option value="3">3 - Good</option>
                            <option value="4">4 - Very Good</option>
                            <option value="5">5 - Excellent</option>
                        </select>
                        <label>Comments:</label>
                        <textarea v-model="review.comments" class="form-control" rows="3"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-primary" @click="submitReview">Submit</button>
                        <button class="btn btn-secondary" @click="closeReviewModal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    `,

    data() {
        return {
            searchQuery: "",
            services: {
                available: [],
                booked: [],
                closed: []
            },
            loading: false,
            error: null,
            showReviewModal: false,
            review: {
                serviceRequestId: null,
                rating: 5,
                comments: "",
            }
        };
    },

    methods: {
        async fetchServices() {
            this.loading = true;
            this.error = null;
        
            try {
                const token = store.getters.authToken;
                if (!token) throw new Error("No authentication token found. Please log in again.");
        
                const response = await fetch("http://127.0.0.1:5000/api/customer/services", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                });
        
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || response.statusText);
        
                this.services.booked = data.filter(service => service.status !== "Closed");
                this.services.closed = data.filter(service => service.status === "Closed");
        
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },

        openReviewModal(serviceRequestId) {
            this.review.serviceRequestId = serviceRequestId;
            this.review.rating = 5;
            this.review.comments = "";
            this.showReviewModal = true;
        },

        closeReviewModal() {
            this.showReviewModal = false;
        },

        async submitReview() {
            try {
                const response = await fetch(`/api/customer/reviews`, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${store.state.token}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify(this.review)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || "Failed to submit review");
                }

                alert("Review submitted successfully.");
                this.closeReviewModal();
            } catch (err) {
                alert(err.message);
            }
        },

        async searchServices() {
            this.loading = true;
            this.error = null;
        
            try {
                const query = this.searchQuery.trim();
                if (!query) {
                    this.error = "Please enter a search term.";
                    this.loading = false;
                    return;
                }
        
                const response = await fetch(`http://127.0.0.1:5000/api/services/search?name=${query}`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${store.getters.authToken}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                });
        
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || response.statusText);
        
                this.services.available = data;
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },

        async bookService(serviceId) {
            if (!confirm("Are you sure you want to book this service?")) return;

            try {
                const response = await fetch(`/api/book_service`, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${store.getters.authToken}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({ service_id: serviceId })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || "Failed to book service");
                }

                alert("Service booked successfully.");
                this.fetchServices();
            } catch (err) {
                alert(err.message);
            }
        },

        async cancelService(serviceId) {
            if (!confirm("Are you sure you want to cancel this service?")) return;

            try {
                const response = await fetch(`/api/customer/services/${serviceId}`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": `Bearer ${store.state.token}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || "Failed to cancel service");
                }

                this.services.booked = this.services.booked.filter(service => service.id !== serviceId);
                alert("Service canceled successfully.");
            } catch (err) {
                alert(err.message);
            }
        },

        async closeService(serviceId) {
            if (!confirm("Are you sure you want to close this service?")) return;

            try {
                const response = await fetch(`/api/customer/services/${serviceId}/close`, {
                    method: "PATCH",
                    headers: {
                        "Authorization": `Bearer ${store.state.token}`,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || "Failed to close service");
                }

                const closedService = this.services.booked.find(service => service.id === serviceId);
                if (closedService) {
                    closedService.status = "Closed";
                    this.services.booked = this.services.booked.filter(service => service.id !== serviceId);
                    this.services.closed.push(closedService);
                }

                alert("Service closed successfully.");
            } catch (err) {
                alert(err.message);
            }
        }
    },

    mounted() {
        this.fetchServices();
    }
};
