export default {
    template: `
    <div class="container mt-5">
        <h2 class="mb-4">Register Page</h2>
        
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" id="username" class="form-control" v-model="username" required />
        </div>
        
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" id="email" class="form-control" v-model="email" required />
        </div>
        
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" id="password" class="form-control" v-model="password" required />
        </div>
        
        <div class="mb-3">
            <label for="role" class="form-label">Select Role:</label>
            <select id="role" class="form-select" v-model="role">
                <option value="customer">Customer</option>
                <option value="service_professional">Service Professional</option>
            </select>
        </div>
        
        <!-- Additional Fields for Customers -->
        <div v-if="role === 'customer'">
            <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" id="address" class="form-control" v-model="address" required />
            </div>
            
            <div class="mb-3">
                <label for="pincode" class="form-label">Pincode</label>
                <input type="text" id="pincode" class="form-control" v-model="pincode" required />
            </div>
        </div>
        
        <!-- Additional Fields for Service Professionals -->
        <div v-if="role === 'service_professional'">
            <div class="mb-3">
                <label for="service_type" class="form-label">Service Type</label>
                <select id="service_type" class="form-select" v-model="service_type" required>
                    <option value="" disabled selected>Select Service Type</option>
                    <option value="Plumber">Plumber</option>
                    <option value="Saloon Service">Saloon Service</option>
                    <option value="Electrician">Electrician</option>
                    <option value="AC Service">AC Service</option>
                </select>
            </div>
            
            <div class="mb-3">
                <label for="experience" class="form-label">Years of Experience</label>
                <input type="number" id="experience" class="form-control" v-model="experience" min="0" required />
            </div>
        </div>

        <button class="btn btn-success w-100" @click="register">Register</button>
    </div>
    `,
    data() {
        return {
            username: '',
            email: '',
            password: '',
            role: 'customer',
            address: '',
            pincode: '',
            service_type: '',
            experience: 0
        };
    },
    methods: {
        async register() {
            try {
                const requestBody = {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    role: this.role
                };

                // Include additional fields if registering as a Customer
                if (this.role === 'customer') {
                    requestBody.address = this.address;
                    requestBody.pincode = this.pincode;
                }

                // Include additional fields if registering as a Service Professional
                if (this.role === 'service_professional') {
                    requestBody.service_type = this.service_type;
                    requestBody.experience = this.experience;
                }
                
                console.log("Sending Request:", requestBody);
                
                const res = await fetch(`${location.origin}/api/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.error || "Registration failed");

                alert('Registered successfully! Please login.');
                window.location.href = '/login';  // Redirect to login page
            } catch (error) {
                alert(error.message);
            }
        }
    }
};
