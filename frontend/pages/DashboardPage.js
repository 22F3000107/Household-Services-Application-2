export default {
    template: `
    <div class="container mt-4">
        <h2 class="mb-3">Dashboard</h2>
        <p>Welcome, {{ role }}!</p>

        <!-- Admin Panel -->
        <div v-if="role === 'admin'" class="mb-3">
            <h3>Admin Panel</h3>
            <div class="d-flex gap-2">
                <button @click="navigate('/admin-users')" class="btn btn-primary">Manage Users</button>
                <button @click="navigate('/admin-services')" class="btn btn-primary">Manage Services</button>
            </div>
        </div>

        <!-- Customer Panel -->
        <div v-if="role === 'customer'" class="mb-3">
            <h3>Customer Panel</h3>
            <div class="d-flex gap-2">
                <button @click="navigate('/book-service')" class="btn btn-success">Book a Service</button>
                <button @click="navigate('/customer-requests')" class="btn btn-success">View My Requests</button>
            </div>
        </div>

        <!-- Service Professional Panel -->
        <div v-if="role === 'professional'" class="mb-3">
            <h3>Service Professional Panel</h3>
            <div class="d-flex gap-2">
                <button @click="navigate('/professional-jobs')" class="btn btn-warning">View Assigned Jobs</button>
                <button @click="navigate('/update-job-status')" class="btn btn-warning">Update Job Status</button>
            </div>
        </div>

        <button class="btn btn-danger mt-3" @click="logout">Logout</button>
    </div>
    `,
    computed: {
        role() {
            return this.$store.state.role; // Get user role from Vuex store
        }
    },
    methods: {
        navigate(route) {
            this.$router.push(route); // Unified function for navigation
        },
        logout() {
            this.$store.dispatch("logout");
            alert("Logged out successfully!");
            this.$router.push("/login");
        }
    }
};
