export default {
    template: `
    <div class="container mt-4">
        <h2>Add New Service</h2>

        <form @submit.prevent="submitService">
            <div class="form-group">
                <label for="serviceName">Service Name:</label>
                <input type="text" id="serviceName" v-model="serviceName" class="form-control" required />
            </div>
            
            <div class="form-group">
                <label for="description">Description:</label>
                <textarea id="description" v-model="description" class="form-control" rows="3"></textarea>
            </div>

            <div class="form-group">
                <label for="basePrice">Base Price:</label>
                <input type="number" id="basePrice" v-model.number="basePrice" class="form-control" />
            </div>

            <div class="form-group">
                <label for="duration">Estimated Time (in hours):</label>
                <input type="number" id="duration" v-model.number="duration" class="form-control"  />
            </div>
            
            <button type="submit" class="btn btn-success mt-3" :disabled="loading">
                {{ loading ? 'Adding...' : 'Add Service' }}
            </button>
            <button @click="goBack" class="btn btn-secondary mt-3 ml-2">Cancel</button>
        </form>

        <p v-if="error" class="text-danger mt-2">{{ error }}</p>
    </div>
    `,
    data() {
        return {
            serviceName: "",
            description: "",
            basePrice: null,
            duration: null,
            loading: false,
            error: null
        };
    },
    methods: {
        async submitService() {
            this.loading = true;
            this.error = null;

            // Trim inputs
            const serviceNameTrimmed = this.serviceName.trim();

            if (!serviceNameTrimmed) {
                this.error = "Service name cannot be empty!";
                this.loading = false;
                return;
            }

            try {
                const response = await fetch("/api/services", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: serviceNameTrimmed,
                        description: this.description,
                        base_price: this.basePrice,
                        time_required: this.duration
                    })
                });

                const result = await response.json();
                if (!response.ok) throw new Error(result.error || "Failed to add service");

                alert("Service added successfully!");
                
                // Reset form fields
                this.serviceName = "";
                this.description = "";
                this.basePrice = null;
                this.duration = null;

                this.$router.push("/admin-services"); // Redirect back
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        goBack() {
            this.$router.push("/admin-services");
        }
    }
};
