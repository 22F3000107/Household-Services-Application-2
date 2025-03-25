// import store from "../utils/store.js";

// export default {
//     template: `
//     <div>
//         <h2>Book a Service</h2>
//         <label for="service-select">Select a service:</label>
//         <select v-model="selectedService" id="service-select">
//             <option disabled value="">-- Choose a service --</option>
//             <option v-for="service in services" :key="service.id" :value="service.id">
//                 {{ service.name }}
//             </option>
//         </select>
//         <button @click="bookService" :disabled="!selectedService">Book</button>
//     </div>
//     `,
//     data() {
//         return {
//             selectedService: "",
//             services: [
//                 { id: 1, name: "AC Repair" },
//                 { id: 2, name: "Electrician" },
//                 { id: 3, name: "House Cleaning" },
//             ]
//         };
//     },
//     methods: {
//         async bookService() {
//             if (!this.selectedService) {
//                 alert("Please select a service.");
//                 return;
//             }

//             try {
//                 const token = store.getters.authToken;

//                 if (!token) {
//                     alert("You must be logged in to book a service.");
//                     return;
//                 }

//                 const response = await fetch("http://127.0.0.1:5000/api/book_service", {
//                     method: "POST",
//                     headers: {
//                         "Content-Type": "application/json",
//                         "Authorization": `Bearer ${token}`,
//                     },
//                     body: JSON.stringify({
//                         service_id: this.selectedService,
//                     }),
//                 });

//                 const data = await response.json();

//                 if (response.ok) {
//                     alert(`Service "${this.selectedServiceName}" booked successfully.`);
//                     this.selectedService = "";  // Reset selection
//                 } else {
//                     alert(`Failed to book service: ${data.error}`);
//                 }
//             } catch (error) {
//                 console.error("Error booking service:", error);
//                 alert("An error occurred while booking the service.");
//             }
//         }
//     }
// };

import store from "../utils/store.js";
export default {
    template: `
    <div class="container mt-4">
        <h2>Available Services</h2>
        <p>Select a service and click "Book" to proceed.</p>

        <p v-if="loading" class="text-info">Loading services...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="services.length > 0" class="table table-striped">
            <thead>
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
                    <td>{{ service.name }}</td>
                    <td>{{ service.description || 'No description available' }}</td>
                    <td>₹{{ service.base_price }}</td>
                    <td>{{ service.time_required > 0 ? service.time_required : 'N/A' }}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" @click="bookService(service.id)">
                            Book
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="services.length === 0 && !loading" class="text-muted">No services available.</p>
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
                const response = await fetch("/api/services");
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || "Failed to fetch services.");
                }

                this.services = data;
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },
        async bookService(serviceId) {
            if (!confirm("Are you sure you want to book this service?")) return;

            try {
                const token = store.getters.authToken;  // Fetch token from store
                const response = await fetch("/api/book_service", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ service_id: serviceId })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Failed to book service.");
                }

                alert("Service booked successfully!");
            } catch (error) {
                alert(error.message);
            }
        }
    },
    mounted() {
        this.fetchServices();
    }
};
