import store from "../store.js"; // Import Vuex store for authentication

export default {
    template: `
    <div class="container mt-4">
        <h2>Manage Services</h2>
        <p>List of available services.</p>

        <p v-if="loading" class="text-info">Loading services...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="services.length > 0" class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Service Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td>{{ service.name }}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" @click="deleteService(service.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="services.length === 0 && !loading" class="text-muted">No services available.</p>

        <button class="btn btn-primary mt-3" @click="addService">Add New Service</button>
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
                const response = await fetch("/api/services", {
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
        async deleteService(serviceId) {
            if (!confirm("Are you sure you want to delete this service?")) return;
            try {
                const response = await fetch(`/api/services/${serviceId}`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${store.state.token}` }
                });

                if (!response.ok) throw new Error("Failed to delete service");

                this.services = this.services.filter(service => service.id !== serviceId);
                alert("Service deleted successfully.");
            } catch (err) {
                alert(err.message);
            }
        },
        addService() {
            this.$router.push("/add-service"); // Navigate to Add Service Page
        }
    },
    mounted() {
        this.fetchServices();
    }
};
