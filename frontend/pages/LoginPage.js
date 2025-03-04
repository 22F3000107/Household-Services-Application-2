// export default {
//     template: `
//     <div>
//         <h2>Login Page</h2>
//         <input type="text" placeholder="email" v-model="email"/>
//         <input type="password" placeholder="password" v-model="password"/>
//         <button class="btn btn-primary" @click="login">Login</button>
//     </div>
//     `,
//     data(){
//         return {
//             email: '',
//             password: ''
//         };
//     },
//     methods: {
//         async login(){
//             const res = await fetch(location.origin+'/api/login', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({
//                     email: this.email,
//                     password: this.password
//                 })
//             });
//             const data = await res.json();
//             if (data.error) {
//                 alert(data.error);
//             } else {
//                localStorage.setItem('token', data.token);  // Save token for future requests
//                 alert('Logged in');
//             }
//         }
//     }
// };


export default {
    template: `
    <div class="container mt-4">
        <h2>Login Page</h2>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" class="form-control" required />
            </div>

            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-primary mt-3">Login</button>
        </form>

       
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
                    'professional': '/professional-dashboard',
                    'customer': '/customer-dashboard'
                };
                window.location.href = roleRoutes[data.role] || '/customer-dashboard';
            } catch (error) {
                alert(error.message);
            }
        }
    }
};
