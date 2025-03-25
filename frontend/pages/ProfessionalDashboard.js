import store from "../utils/store.js";

export default {
    template: `
    <div class="container mt-4">
        <h2>Professional Dashboard</h2>
        <p>Manage your assigned jobs.</p>

        <p v-if="loading" class="text-info">Loading your jobs...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="jobs.length > 0" class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Service Name</th>
                    <th>Customer Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="job in jobs" :key="job.id">
                    <td>{{ job.id }}</td>
                    <td>{{ job.service_name }}</td>
                    <td>{{ job.customer_name || "Unknown" }}</td>
                    <td>{{ job.status }}</td>
                    <td>
                        <!-- Accept & Reject for 'requested' services -->
                        <button @click="updateStatus(job.id, 'accept')" v-if="job.status === 'requested'" class="btn btn-success btn-sm">
                            Accept
                        </button>
                        <button @click="updateStatus(job.id, 'reject')" v-if="job.status === 'requested'" class="btn btn-danger btn-sm">
                            Reject
                        </button>

                        <!-- Mark as Completed for 'assigned' services -->
                        <button @click="updateStatus(job.id, 'complete')" v-if="job.status === 'assigned'" class="btn btn-primary btn-sm">
                            Mark as Completed
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="!loading && jobs.length === 0" class="text-muted">No service requests found.</div>
    </div>
    `,
    data() {
        return {
            jobs: [],
            loading: false,
            error: null,
        };
    },
    methods: {
        async fetchJobs() {
            console.log("Fetching Jobs...");

            if (!store.state.token) {
                this.error = "Not authenticated. Please log in.";
                return;
            }

            this.loading = true;
            this.error = null;

            try {
                const response = await fetch("/api/service_requests/professional", {
                    headers: { 
                        Authorization: `Bearer ${store.state.token}`,
                        "Content-Type": "application/json"
                    }
                });

                if (!response.ok) throw new Error("Failed to fetch jobs");

                this.jobs = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },

        async updateStatus(jobId, action) {
            if (!store.state.token) {
                alert("Authentication required. Please log in.");
                return;
            }

            try {
                const response = await fetch(`/api/service_requests/${jobId}/${action}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${store.state.token}`
                    }
                });

                if (!response.ok) {
                    const errorMsg = await response.text();
                    throw new Error(errorMsg || "Failed to update status");
                }

                // Refresh job list after action
                await this.fetchJobs(); 

                alert(`Job ${this.getActionLabel(action)} successfully.`);
            } catch (err) {
                alert(`Error: ${err.message}`);
            }
        },

        getActionLabel(action) {
            return action === "accept" ? "accepted" :
                   action === "reject" ? "rejected" :
                   action === "complete" ? "marked as completed" : "updated";
        }
    },
    mounted() {
        this.fetchJobs();
    }
};
