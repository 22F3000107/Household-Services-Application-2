import store from "../store.js"; 

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
                    <th>Service</th>
                    <th>Customer</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="job in jobs" :key="job.id">
                    <td>{{ job.id }}</td>
                    <td>{{ job.service_name }}</td>
                    <td>{{ job.customer_name }}</td>
                    <td>{{ job.status }}</td>
                    <td>
                        <button class="btn btn-success btn-sm" @click="updateStatus(job.id, 'Completed')">Mark Completed</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="jobs.length === 0 && !loading" class="text-muted">No assigned jobs.</p>
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
            this.loading = true;
            this.error = null;
            try {
                const response = await fetch(`/api/professional/jobs`, {
                    headers: { Authorization: `Bearer ${store.state.token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch jobs");
                this.jobs = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        async updateStatus(jobId, status) {
            try {
                const response = await fetch(`/api/professional/jobs/${jobId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${store.state.token}`
                    },
                    body: JSON.stringify({ status })
                });

                if (!response.ok) throw new Error("Failed to update status");

                this.jobs = this.jobs.map(job => 
                    job.id === jobId ? { ...job, status } : job
                );

                alert("Job status updated.");
            } catch (err) {
                alert(err.message);
            }
        }
    },
    mounted() {
        this.fetchJobs();
    }
};
