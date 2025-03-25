import store from "../utils/store.js";

export default {
    template: `
    <div class="container mt-4">
        <h2>Admin Dashboard</h2>
        <p>Welcome, Admin! Manage your platform here.</p>

        <div class="row">
            <div class="col-md-4">
                <router-link to="/admin-users" class="btn btn-primary btn-block">Manage Users</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/admin-services" class="btn btn-primary btn-block">Manage Services</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/add-service" class="btn btn-success btn-block">➕ Add New Service</router-link>
            </div>
        </div>

        <hr>

        <h3>Recent Reviews</h3>
        <p v-if="loadingReviews" class="text-info">Loading reviews...</p>
        <p v-if="errorReviews" class="text-danger">{{ errorReviews }}</p>

        <table v-if="reviews.length > 0" class="table table-bordered mt-3">
            <thead class="thead-dark">
                <tr>
                    <th>Customer</th>
                    <th>Professional</th>
                    <th>Rating</th>
                    <th>Comment</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="review in reviews" :key="review.id">
                    <td>{{ review.customer_name }}</td>
                    <td>{{ review.professional_name }}</td>
                    <td>{{ review.rating }}</td>
                    <td>{{ review.comment }}</td>
                </tr>
            </tbody>
        </table>

        <div v-if="!loadingReviews && reviews.length === 0" class="text-muted">
            No recent reviews.
        </div>

        <hr>

        <h3>Search Professionals</h3>
        <input v-model="searchQuery" placeholder="Search professionals..." class="form-control">
        <button @click="searchProfessionals" class="btn btn-primary mt-2">Search</button>
        
        <ul v-if="professionals.length">
            <li v-for="prof in professionals" :key="prof.id">
                {{ prof.name }} ({{ prof.email }}) - {{ prof.service_type }}
                <button @click="blockProfessional(prof.id)" v-if="!prof.is_blocked" class="btn btn-danger btn-sm">Block</button>
                <button @click="unblockProfessional(prof.id)" v-if="prof.is_blocked" class="btn btn-success btn-sm">Unblock</button>
            </li>
        </ul>
        <p v-if="error" class="text-danger">{{ error }}</p>


        <hr>

        <h3>Pending Service Professionals</h3>
        <p v-if="loading" class="text-info">Loading pending professionals...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="pendingProfessionals.length > 0" class="table table-bordered mt-3">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Service Type</th>
                    <th>Experience</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="prof in pendingProfessionals" :key="prof.id">
                    <td>{{ prof.id }}</td>
                    <td>{{ prof.name }}</td>
                    <td>{{ prof.email }}</td>
                    <td>{{ prof.service_type }}</td>
                    <td>{{ prof.experience }}</td>
                    <td>
                        <button @click="approveProfessional(prof.id)" class="btn btn-success btn-sm">Approve</button>
                        <button @click="rejectProfessional(prof.id)" class="btn btn-danger btn-sm ml-2">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="!loading && pendingProfessionals.length === 0" class="text-muted">
            No pending service professionals.
        </div>

        <hr>

        <h3>Assign Service Requests to Professionals</h3>
        <p v-if="loadingRequests" class="text-info">Loading service requests...</p>
        <p v-if="errorRequests" class="text-danger">{{ errorRequests }}</p>

        <table v-if="unassignedRequests.length > 0" class="table table-bordered mt-3">
            <thead class="thead-dark">
                <tr>
                    <th>Request ID</th>
                    <th>Service</th>
                    <th>Customer Name</th>
                    <th>Status</th>
                    <th>Assign to Professional</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in unassignedRequests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.service_name }}</td>
                    <td>{{ request.customer_name }}</td>
                    <td>{{ request.status }}</td>
                    <td>
                        <select v-model="selectedProfessional[request.id]" class="form-control">
                            <option value="">Select Professional</option>
                            <option v-for="pro in approvedProfessionals" :key="pro.id" :value="pro.id">
                                {{ pro.name }} ({{ pro.service_type }})
                            </option>
                        </select>
                        <button @click="assignJob(request.id)" class="btn btn-primary btn-sm mt-2">
                            Assign
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="!loadingRequests && unassignedRequests.length === 0" class="text-muted">
            No unassigned service requests.
        </div>
    </div>
    `,
    data() {
        return {
            searchQuery: "",
            professionals: [],
            pendingProfessionals: [],
            approvedProfessionals: [],
            unassignedRequests: [],
            selectedProfessional: {},
            reviews: [],
            loading: false,
            loadingRequests: false,
            loadingReviews: false,
            error: null,
            errorRequests: null,
            errorReviews: null,
        };
    },
    methods: {
        async fetchReviews() {
            try {
                this.loadingReviews = true;
                const response = await fetch("/api/admin/reviews", {
                    headers: { "Authorization": `Bearer ${store.state.token}` }
                });
                if (!response.ok) throw new Error("Failed to fetch reviews");
                this.reviews = await response.json();
            } catch (error) {
                this.errorReviews = error.message;
            } finally {
                this.loadingReviews = false;
            }
        },

        async searchProfessionals() {
            try {
                const params = new URLSearchParams();
                if (this.searchQuery) params.append("name", this.searchQuery);
                if (this.searchEmail) params.append("email", this.searchEmail);
                if (this.searchServiceType) params.append("service_type", this.searchServiceType);

                console.log("🔍 Sending request:", `/api/professionals/search?${params.toString()}`);

        
                const response = await fetch(`/api/professionals/search?${params.toString()}`, {
                    headers: { Authorization: `Bearer ${store.state.token}` }
                });
        
                if (!response.ok) throw new Error("Failed to fetch professionals");
        
                this.professionals = await response.json();
                console.log("✅ Response Data:", this.professionals);
            } catch (err) {
                this.error = err.message;
            }
        },
        

       
        async fetchPendingProfessionals() {
            try {
                const token = this.$store.getters.authToken; // Get token from Vuex
        
                if (!token) {
                    console.warn("Admin token missing.");
                    alert("Session expired! Please log in again.");
                    return;
                }
        
                const response = await fetch("http://127.0.0.1:5000/api/admin/pending_professionals", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });
        
                if (!response.ok) {
                    const errorResponse = await response.json();
                    console.error("Server Error:", errorResponse);
                    throw new Error(errorResponse.error || "Failed to fetch professionals");
                }
        
                const data = await response.json();
                this.pendingProfessionals = data;
            } catch (error) {
                console.error("Error fetching professionals:", error.message);
            }
        },

        async approveProfessional(professionalId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/admin/approved_professionals/${professionalId}`, {
                    method: "PATCH",
                    headers: {
                        "Authorization": `Bearer ${this.$store.getters.authToken}`,
                        "Content-Type": "application/json",
                    },
                });
        
                if (!response.ok) throw new Error("Approval failed");
        
                alert("Professional approved successfully.");
                this.fetchPendingProfessionals();
                this.fetchApprovedProfessionals();
            } catch (error) {
                console.error("Error approving professional:", error);
            }
        },
        
        async rejectProfessional(professionalId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/admin/reject_professional/${professionalId}`, {
                    method: "PATCH",
                    headers: {
                        "Authorization": `Bearer ${this.$store.getters.authToken}`,
                        "Content-Type": "application/json",
                    },
                });
        
                if (!response.ok) throw new Error("Rejection failed");
        
                alert("Professional rejected.");
                this.fetchPendingProfessionals();
            } catch (error) {
                console.error("Error rejecting professional:", error);
            }
        },
        
        async fetchApprovedProfessionals() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/admin/approved_professionals", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${this.$store.getters.authToken}`,
                        "Content-Type": "application/json",
                    },
                });
        
                if (!response.ok) throw new Error("Failed to fetch approved professionals");
        
                this.approvedProfessionals = await response.json();
            } catch (error) {
                console.error("Error fetching approved professionals:", error);
            }
        },
        
        async fetchUnassignedRequests() {
            try {
                const response = await fetch("/api/admin/unassigned_requests", {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${this.$store.getters.authToken}` },
                });
        
                if (!response.ok) throw new Error("Failed to fetch service requests");
        
                this.unassignedRequests = await response.json();
            } catch (error) {
                console.error("Error fetching service requests:", error);
            }
        },
        
        

        async assignJob(requestId) {
            let professionalId = this.selectedProfessional[requestId];
            if (!professionalId) {
                alert("Please select a professional.");
                return;
            }

            try {
                const response = await fetch(`/api/admin/assign_request/${requestId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${store.state.token}`,
                    },
                    body: JSON.stringify({ professional_id: professionalId }),
                });

                if (!response.ok) throw new Error("Assignment failed");

                alert("Service request assigned successfully!");
                this.fetchUnassignedRequests();
            } catch (error) {
                alert(error.message);
            }
        }
    },
    mounted() {
        this.fetchPendingProfessionals();
        this.fetchApprovedProfessionals();
        this.fetchUnassignedRequests();
        this.fetchReviews();
    }
};

