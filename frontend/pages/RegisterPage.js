// export default {
//     template: `
//     <div>
//         <input type="text" placeholder="Username" v-model="username"/>  
//         <input type="text" placeholder="Email" v-model="email"/>
//         <input type="password" placeholder="Password" v-model="password"/>
        
//         <label for="role">Select Role:</label>
//         <select id="role" v-model="role">
//             <option value="customer">Customer</option>
//             <option value="professional">Service Professional</option>
//         </select>

//         <button @click="register">Register</button>
//     </div>
//     `,
//     data(){
//         return {
//             username: '',  
//             email: '',
//             password: '',
//             role : 'customer' // Default role
//         }
//     },
//     methods: {
//         async register(){
//             const res = await fetch(location.origin+'/api/register', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({
//                     'username': this.username,  
//                     'email': this.email,
//                     'password': this.password,
//                     'role' : this.role
//                 })
//             })
//             const data = await res.json();
//             if(res.ok){
//                 alert('Registered successfully!')
//             } else {
//                 alert(data.error)
//             }
//         }
//     }
// }


export default {
    template: `
    <div class="container mt-5">
        <h2 class="mb-4">Register</h2>
        <div class="mb-3">
            <input type="text" class="form-control" placeholder="Username" v-model="username" required />
        </div>
        <div class="mb-3">
            <input type="email" class="form-control" placeholder="Email" v-model="email" required />
        </div>
        <div class="mb-3">
            <input type="password" class="form-control" placeholder="Password" v-model="password" required />
        </div>
        <div class="mb-3">
            <label for="role" class="form-label">Select Role:</label>
            <select id="role" class="form-select" v-model="role">
                <option value="customer">Customer</option>
                <option value="professional">Service Professional</option>
            </select>
        </div>
        <button class="btn btn-success w-100" @click="register">Register</button>
    </div>
    `,
    data() {
        return {
            username: '',
            email: '',
            password: '',
            role: 'customer'
        };
    },
    methods: {
        async register() {
            try {
                const res = await fetch(`${location.origin}/api/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: this.username,
                        email: this.email,
                        password: this.password,
                        role: this.role
                    })
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
