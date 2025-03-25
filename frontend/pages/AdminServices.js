import store from "../utils/store.js";

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
                    <th>Description</th>
                    <th>Base Price</th>
                    <th>Time Required(hrs)</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in services" :key="service.id">
                    <td>{{ service.id }}</td>
                    <td v-if="!service.editing">{{ service.name }}</td>
                    <td v-else><input v-model="service.name" class="form-control" /></td>

                    <td v-if="!service.editing">{{ service.description || 'No description available' }}</td>
                    <td v-else><input v-model="service.description" class="form-control" /></td>

                    <td v-if="!service.editing">{{ service.base_price }}</td>
                    <td v-else><input v-model.number="service.base_price" type="number" class="form-control" /></td>

                    <td v-if="!service.editing">{{ service.time_required > 0 ? service.time_required : 'N/A' }}</td>
                    <td v-else><input v-model="service.time_required" type="number" class="form-control" /></td>

                    <td>
                        <button v-if="!service.editing" class="btn btn-warning btn-sm" @click="editService(service)">Edit</button>
                        <button v-if="service.editing" class="btn btn-success btn-sm" @click="updateService(service)">Update</button>
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

                const data = await response.json();
                console.log("Fetched services (raw):", JSON.stringify(data, null, 2));

                // Process services to handle missing fields
                this.services = data.map(service => ({
                    id: service.id,
                    name: service.name,
                    description: service.description || "No description available",
                    base_price: service.base_price,
                    time_required: service.time_required > 0 ? service.time_required : "N/A",
                    editing: false // Track edit mode
                }));

                console.log("Fetched services (processed):", this.services);
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
        editService(service) {
            service.editing = true;
        },
        async updateService(service) {
            try {
                const response = await fetch(`/api/services/${service.id}`, {
                    method: "PUT",
                    headers: { 
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${store.state.token}` 
                    },
                    body: JSON.stringify({
                        name: service.name,
                        description: service.description,
                        base_price: service.base_price,
                        time_required: service.time_required
                    })
                });

                if (!response.ok) throw new Error("Failed to update service");

                alert("Service updated successfully.");
                service.editing = false;
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
