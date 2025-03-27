// import store from "../utils/store.js";

// export default {
//     template: `
//     <div class="container mt-5 pt-4">
//         <h2 class="text-info">Professional Dashboard</h2>
//         <p class="text-muted">Manage your assigned jobs.</p>

//         <p v-if="loading" class="text-info">Loading your jobs...</p>
//         <p v-if="error" class="text-danger">{{ error }}</p>

//         <table v-if="jobs.length > 0" class="table table-bordered">
//             <thead class="thead-dark">
//                 <tr>
//                     <th>ID</th>
//                     <th>Service Name</th>
//                     <th>Customer Name</th>
//                     <th>Address</th>
//                     <th>Status</th>
//                     <th>Actions</th>
//                 </tr>
//             </thead>
//             <tbody>
//                 <tr v-for="job in jobs" :key="job.id">
//                     <td>{{ job.id }}</td>
//                     <td>{{ job.service_name || "Unknown" }}</td>
//                     <td>{{ job.customer_name || "Unknown" }}</td>
//                     <td>{{ job.customer_address || "Unknown" }}</td>
//                     <td>{{ job.status }}</td>
//                     <td>
//                         <button @click="updateStatus(job.id, 'accept')" v-if="job.status === 'requested'" class="btn btn-success btn-sm">
//                             Accept
//                         </button>
//                         <button @click="updateStatus(job.id, 'reject')" v-if="job.status === 'requested'" class="btn btn-danger btn-sm">
//                             Reject
//                         </button>
//                         <button @click="updateStatus(job.id, 'complete')" v-if="job.status === 'assigned'" class="btn btn-primary btn-sm">
//                             Mark as Completed
//                         </button>
//                     </td>
//                 </tr>
//             </tbody>
//         </table>

//         <div v-if="!loading && jobs.length === 0" class="text-muted">No service requests found.</div>
//     </div>
//     `,
//     data() {
//         return {
//             jobs: [],
//             loading: false,
//             error: null,
//         };
//     },
//     methods: {
//         async fetchJobs() {
//             console.log("Fetching Jobs...");

//             if (!store.state.token) {
//                 this.error = "Not authenticated. Please log in.";
//                 return;
//             }

//             this.loading = true;
//             this.error = null;

//             try {
//                 const response = await fetch("/api/service_requests/professional", {
//                     headers: { 
//                         Authorization: `Bearer ${store.state.token}`,
//                         "Content-Type": "application/json"
//                     }
//                 });

//                 if (!response.ok) throw new Error("Failed to fetch jobs");

//                 const responseData = await response.json();
//                 console.log("API Response:", responseData);

//                 this.jobs = responseData.map(job => ({
//                     ...job,
//                     service_name: job.service_name || "Unknown"  // Ensure service_name is never null
//                 }));

//                 this.jobs = [...this.jobs];  // Force Vue to detect reactivity changes

//             } catch (err) {
//                 this.error = err.message;
//             } finally {
//                 this.loading = false;
//             }
//         },

//         async updateStatus(jobId, action) {
//             if (!store.state.token) {
//                 alert("Authentication required. Please log in.");
//                 return;
//             }

//             let requestBody = {};

//              // If the action is "complete", ask for remarks
//              if (action === "complete") {
//                 const remarks = prompt("Enter remarks before closing (optional):");
//                 requestBody.remarks = remarks || "";
//             }

//             try {
//                 const response = await fetch(`/api/service_requests/${jobId}/${action}`, {
//                     method: "PUT",
//                     headers: {
//                         "Content-Type": "application/json",
//                         Authorization: `Bearer ${store.state.token}`
//                     },
//                     body: JSON.stringify(requestBody)  // Send remarks only for "complete"
//                 });

//                 if (!response.ok) {
//                     const errorMsg = await response.text();
//                     throw new Error(errorMsg || "Failed to update status");
//                 }

//                 await this.fetchJobs();  // Refresh jobs after status update

//                 alert(`Job ${this.getActionLabel(action)} successfully.`);
//             } catch (err) {
//                 alert(`Error: ${err.message}`);
//             }
//         },

//         getActionLabel(action) {
//             return action === "accept" ? "accepted" :
//                    action === "reject" ? "rejected" :
//                    action === "complete" ? "marked as completed" : "updated";
//         }
//     },
//     mounted() {
//         this.fetchJobs();
//     }
// };

import store from "../utils/store.js";

export default {
    template: `
    <div class="container mt-5 pt-4">
        <h2 class="text-info">Professional Dashboard</h2>
        <p class="text-muted">Manage your assigned jobs.</p>

        <p v-if="loading" class="text-info">Loading your jobs...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>

        <table v-if="jobs.length > 0" class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Service Name</th>
                    <th>Customer Name</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="job in jobs" :key="job.id">
                    <td>{{ job.id }}</td>
                    <td>{{ job.service_name || "Unknown" }}</td>
                    <td>{{ job.customer_name || "Unknown" }}</td>
                    <td>{{ job.customer_address || "Unknown" }}</td>
                    <td>{{ job.status }}</td>
                    <td>
                        <button @click="updateStatus(job.id, 'accept')" v-if="job.status === 'assigned'" class="btn btn-success btn-sm">
                            Accept
                        </button>
                        <button @click="updateStatus(job.id, 'reject')" v-if="job.status === 'assigned'" class="btn btn-danger btn-sm">
                            Reject
                        </button>
                        <button @click="updateStatus(job.id, 'complete')" v-if="job.status === 'accepted'" class="btn btn-primary btn-sm">
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

                const responseData = await response.json();
                console.log("API Response:", responseData);

                this.jobs = responseData.map(job => ({
                    ...job,
                    service_name: job.service_name || "Unknown"  // Ensure service_name is never null
                }));

                this.jobs = [...this.jobs];  // Force Vue to detect reactivity changes

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

            let requestBody = {};

            // If the action is "complete", ask for remarks
            if (action === "complete") {
                const remarks = prompt("Enter remarks before closing (optional):");
                requestBody.remarks = remarks || "";
            }

            console.log("🔍 Sending request to:", `/api/service_requests/${jobId}/${action}`);
            console.log("🔍 Request body:", JSON.stringify(requestBody));


            try {
                const response = await fetch(`/api/service_requests/${jobId}/${action}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${store.state.token}`
                    },
                    body: JSON.stringify(requestBody)   // Send remarks only for "complete"
                });

                console.log("🔍 Response status:", response.status);


                if (!response.ok) {
                    const errorMsg = await response.text();
                    console.error("❌ Error response:", errorMsg);
                    throw new Error(errorMsg || "Failed to update status");
                }

                await this.fetchJobs();  // Refresh jobs after status update

                alert(`Job ${this.getActionLabel(action)} successfully.`);
            } catch (err) {
                console.error("❌ Request failed:", err.message);
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
