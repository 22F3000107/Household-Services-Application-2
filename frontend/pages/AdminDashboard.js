export default {
    template: `
    <div class="container mt-4">
        <h2>Admin Dashboard</h2>
        <p>Welcome, Admin! Manage your platform here.</p>

        <div class="row">
            <div class="col-md-4">
                <router-link to="/admin-users" class="btn btn-primary btn-block">Manage Users</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/admin-services" class="btn btn-primary btn-block">Manage Services</router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/add-service" class="btn btn-success btn-block">➕ Add New Service</router-link>
            </div>
        </div>
    </div>
    `
};
