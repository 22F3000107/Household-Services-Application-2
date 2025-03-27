export default {
    template: `
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
        <div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
            <h2 class="text-center mb-4">Login</h2>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input type="email" id="email" v-model="email" class="form-control" placeholder="Enter your email" required />
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input type="password" id="password" v-model="password" class="form-control" placeholder="Enter your password" required />
                </div>

                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
        </div>
    </div>
    `,
    data() {
        return {
            email: '',
            password: ''
        };
    },
    methods: {
        async login() {
            try {
                const res = await fetch(`${location.origin}/api/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: this.email, password: this.password })
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.error || "Login failed");

                localStorage.setItem('token', data.token);
                localStorage.setItem('role', data.role);
                alert('Logged in successfully');

                // Redirect based on role
                const roleRoutes = {
                    'admin': '/admin-dashboard',
                    'service_professional': '/professional-dashboard',
                    'customer': '/customer-dashboard'
                };
                window.location.href = roleRoutes[data.role] || '/customer-dashboard';
            } catch (error) {
                alert(error.message);
            }
        }
    }
};
