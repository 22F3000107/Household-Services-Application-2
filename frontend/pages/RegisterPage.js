// export default {
//     template: `
//     <div>
//         <input type="text" placeholder="Username" v-model="username"/>  
//         <input type="text" placeholder="Email" v-model="email"/>
//         <input type="password" placeholder="Password" v-model="password"/>
//         <input type="text" placeholder="Role" v-model="role"/>
//         <button @click="register">Register</button>
//     </div>
//     `,
//     data(){
//         return {
//             username: '',  
//             email: '',
//             password: '',
//             role : ''
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
//                 alert('Registered')
//             }else{
//                 alert(data.error)
//             }
//         }
//     }
// }

export default {
    template: `
    <div>
        <input type="text" placeholder="Username" v-model="username"/>  
        <input type="text" placeholder="Email" v-model="email"/>
        <input type="password" placeholder="Password" v-model="password"/>
        
        <label for="role">Select Role:</label>
        <select id="role" v-model="role">
            <option value="customer">Customer</option>
            <option value="professional">Service Professional</option>
        </select>

        <button @click="register">Register</button>
    </div>
    `,
    data(){
        return {
            username: '',  
            email: '',
            password: '',
            role : 'customer' // Default role
        }
    },
    methods: {
        async register(){
            const res = await fetch(location.origin+'/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': this.username,  
                    'email': this.email,
                    'password': this.password,
                    'role' : this.role
                })
            })
            const data = await res.json();
            if(res.ok){
                alert('Registered successfully!')
            } else {
                alert(data.error)
            }
        }
    }
}
