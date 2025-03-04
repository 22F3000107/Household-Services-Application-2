import store from "../store.js"; 

export default {
    template: `
    <div class="container mt-4">
        <h2>Customer Dashboard</h2>
        <p>Manage your booked services.</p>

        <p v-if="loading" class="text-info">Loading your services...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="services.length > 0" class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.name }}</td>
                    <td>{{ service.status }}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" @click="cancelService(service.id)">Cancel</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="services.length === 0 && !loading" class="text-muted">No booked services.</p>
    </div>
    `,
    data() {
        return {
            services: [],
            loading: false,
            error: null,
        };
    },
    methods: {
        async fetchServices() {
            this.loading = true;
            this.error = null;
            try {
                const response = await fetch(`/api/customer/services`, {
                    headers: { Authorization: `Bearer ${store.state.token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch services");
                this.services = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        async cancelService(serviceId) {
            if (!confirm("Are you sure you want to cancel this service?")) return;
            try {
                const response = await fetch(`/api/customer/services/${serviceId}`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${store.state.token}` }
                });

                if (!response.ok) throw new Error("Failed to cancel service");

                this.services = this.services.filter(service => service.id !== serviceId);
                alert("Service canceled successfully.");
            } catch (err) {
                alert(err.message);
            }
        }
    },
    mounted() {
        this.fetchServices();
    }
};
