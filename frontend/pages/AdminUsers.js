export default {
    template: `
    <div class="container mt-4">
        <h2>Manage Users</h2>
        <p>List of all registered users.</p>

        <table class="table table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.role }}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" @click="blockUser(user.id)">Block</button>
                        <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="loading">Loading users...</p>
        <p v-if="error" class="text-danger">{{ error }}</p>
    </div>
    `,
    data() {
        return {
            users: [],
            loading: false,
            error: null,
        };
    },
    methods: {
        async fetchUsers() {
            this.loading = true;
            this.error = null;
            try {
                const response = await fetch("/api/users");
                if (!response.ok) throw new Error("Failed to fetch users");
                this.users = await response.json();
            } catch (err) {
                this.error = err.message;
            } finally {
                this.loading = false;
            }
        },
        async blockUser(userId) {
            if (!confirm("Are you sure you want to block this user?")) return;
            try {
                const response = await fetch(`/api/users/${userId}/block`, { method: "POST" });
                if (!response.ok) throw new Error("Failed to block user");
                this.users = this.users.map(user =>
                    user.id === userId ? { ...user, status: "Blocked" } : user
                );
                alert("User blocked successfully.");
            } catch (err) {
                alert(err.message);
            }
        },
        async deleteUser(userId) {
            if (!confirm("Are you sure you want to delete this user?")) return;
            try {
                const response = await fetch(`/api/users/${userId}`, { method: "DELETE" });
                if (!response.ok) throw new Error("Failed to delete user");
                this.users = this.users.filter(user => user.id !== userId);
                alert("User deleted successfully.");
            } catch (err) {
                alert(err.message);
            }
        },
    },
    mounted() {
        this.fetchUsers();
    }
};

